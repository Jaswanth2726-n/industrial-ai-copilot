
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"

static const char *TAG = "MOTOR_SIMULATOR";

// Generate a random floating-point value between min and max
static float random_float(float min, float max)
{
    return min + ((float)rand() / (float)RAND_MAX) * (max - min);
}

// Periodic motor sensor simulation task
static void motor_sensor_task(void *pvParameters)
{
    srand((unsigned int)time(NULL));

    while (1)
    {
        float temperature_c = random_float(45.0f, 75.0f);
        float vibration_mm_s = random_float(0.5f, 3.0f);
        float rpm = random_float(1400.0f, 1500.0f);
        float current_a = random_float(2.0f, 5.0f);

        printf("{\"temperature_c\": %.2f, \"vibration_mm_s\": %.2f, \"rpm\": %.2f, \"current_a\": %.2f}\n",
            temperature_c,
            vibration_mm_s,
            rpm,
            current_a);

        // Wait 2 seconds before generating the next reading
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}

void app_main(void)
{
    ESP_LOGI(TAG, "Industrial Motor Simulator Started");

    xTaskCreate(
        motor_sensor_task,
        "motor_sensor_task",
        4096,
        NULL,
        5,
        NULL
    );
}
