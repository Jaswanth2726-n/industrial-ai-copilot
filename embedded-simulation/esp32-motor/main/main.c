
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"

#include "esp_log.h"
#include "esp_err.h"
#include "esp_random.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "esp_wifi.h"
#include "nvs_flash.h"
#include "mqtt_client.h"

#define WIFI_SSID       "Wokwi-GUEST"
#define WIFI_PASSWORD   ""

#define MQTT_BROKER_URI "mqtt://test.mosquitto.org:1883"
#define MQTT_TOPIC      "industrial-ai-copilot/demo-esp32-7f3a/motor/sensors"

#define WIFI_CONNECTED_BIT BIT0

static const char *TAG = "INDUSTRIAL_AI";
static EventGroupHandle_t wifi_event_group;
static esp_mqtt_client_handle_t mqtt_client = NULL;

static float random_float(float min, float max)
{
    float random_value = (float)esp_random() / (float)UINT32_MAX;
    return min + random_value * (max - min);
}

static void wifi_event_handler(
    void *arg,
    esp_event_base_t event_base,
    int32_t event_id,
    void *event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START)
    {
        esp_wifi_connect();
    }
    else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED)
    {
        ESP_LOGW(TAG, "Wi-Fi disconnected. Reconnecting...");
        xEventGroupClearBits(wifi_event_group, WIFI_CONNECTED_BIT);
        esp_wifi_connect();
    }
    else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP)
    {
        ESP_LOGI(TAG, "Wi-Fi connected and IP address obtained");
        xEventGroupSetBits(wifi_event_group, WIFI_CONNECTED_BIT);
    }
}

static void wifi_init(void)
{
    wifi_event_group = xEventGroupCreate();

    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    esp_netif_create_default_wifi_sta();

    wifi_init_config_t wifi_init_config = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&wifi_init_config));

    ESP_ERROR_CHECK(
        esp_event_handler_register(
            WIFI_EVENT,
            ESP_EVENT_ANY_ID,
            &wifi_event_handler,
            NULL
        )
    );

    ESP_ERROR_CHECK(
        esp_event_handler_register(
            IP_EVENT,
            IP_EVENT_STA_GOT_IP,
            &wifi_event_handler,
            NULL
        )
    );

    wifi_config_t wifi_config = {0};

    strncpy(
        (char *)wifi_config.sta.ssid,
        WIFI_SSID,
        sizeof(wifi_config.sta.ssid) - 1
    );

    strncpy(
        (char *)wifi_config.sta.password,
        WIFI_PASSWORD,
        sizeof(wifi_config.sta.password) - 1
    );

    wifi_config.sta.threshold.authmode = WIFI_AUTH_OPEN;

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "Connecting to Wokwi Wi-Fi...");

    xEventGroupWaitBits(
        wifi_event_group,
        WIFI_CONNECTED_BIT,
        pdFALSE,
        pdTRUE,
        portMAX_DELAY
    );
}

static void mqtt_event_handler(
    void *handler_args,
    esp_event_base_t base,
    int32_t event_id,
    void *event_data)
{
    if (event_id == MQTT_EVENT_CONNECTED)
    {
        ESP_LOGI(TAG, "Connected to MQTT broker");
    }
    else if (event_id == MQTT_EVENT_DISCONNECTED)
    {
        ESP_LOGW(TAG, "Disconnected from MQTT broker");
    }
    else if (event_id == MQTT_EVENT_ERROR)
    {
        ESP_LOGE(TAG, "MQTT connection error");
    }
}

static void mqtt_init(void)
{
    const esp_mqtt_client_config_t mqtt_config = {
        .broker.address.uri = MQTT_BROKER_URI,
    };

    mqtt_client = esp_mqtt_client_init(&mqtt_config);

    if (mqtt_client == NULL)
    {
        ESP_LOGE(TAG, "Failed to initialize MQTT client");
        return;
    }

    ESP_ERROR_CHECK(
        esp_mqtt_client_register_event(
            mqtt_client,
            ESP_EVENT_ANY_ID,
            mqtt_event_handler,
            NULL
        )
    );

    ESP_ERROR_CHECK(esp_mqtt_client_start(mqtt_client));
}

static void motor_sensor_task(void *pvParameters)
{
    unsigned int sample_count = 0;

    while (1)
    {
        sample_count++;

        bool fault_mode = (sample_count % 10 == 0);

        float temperature_c;
        float vibration_mm_s;
        float rpm;
        float current_a;

        if (fault_mode)
        {
            temperature_c = random_float(82.0f, 95.0f);
            vibration_mm_s = random_float(5.0f, 8.0f);
            rpm = random_float(1250.0f, 1400.0f);
            current_a = random_float(5.5f, 7.0f);
        }
        else
        {
            temperature_c = random_float(63.0f, 68.0f);
            vibration_mm_s = random_float(1.5f, 2.5f);
            rpm = random_float(1470.0f, 1530.0f);
            current_a = random_float(4.0f, 5.0f);
        }

        char payload[256];

        snprintf(
            payload,
            sizeof(payload),
            "{\"mode\":\"%s\",\"temperature_c\":%.2f,"
            "\"vibration_mm_s\":%.2f,\"rpm\":%.2f,\"current_a\":%.2f}",
            fault_mode ? "fault" : "normal",
            temperature_c,
            vibration_mm_s,
            rpm,
            current_a
        );

        printf("Motor sensor data: %s\n", payload);

        if (mqtt_client != NULL)
        {
            int message_id = esp_mqtt_client_publish(
                mqtt_client,
                MQTT_TOPIC,
                payload,
                0,
                1,
                0
            );

            if (message_id >= 0)
            {
                ESP_LOGI(TAG, "MQTT message published: ID=%d", message_id);
            }
            else
            {
                ESP_LOGW(TAG, "MQTT publish failed; will retry next sample");
            }
        }

        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}

void app_main(void)
{
    ESP_LOGI(TAG, "Industrial AI Motor Simulator Starting");

    esp_err_t ret = nvs_flash_init();

    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND)
    {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }

    ESP_ERROR_CHECK(ret);

    wifi_init();
    mqtt_init();

    xTaskCreate(
        motor_sensor_task,
        "motor_sensor_task",
        4096,
        NULL,
        5,
        NULL
    );
}
