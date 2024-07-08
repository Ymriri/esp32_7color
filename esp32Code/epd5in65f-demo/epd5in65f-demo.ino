// #include "DEV_Config.h" // init
#include "EPD.h"
#include "GUI_Paint.h"
#include <stdlib.h>
#include <WiFi.h>

// #include "EPD_5in65f.h"
// #include "EPD_5in65f.cpp"

#include <HTTPClient.h>
#include "esp_http_client.h" // httpclient
#include <stdlib.h>

#include <Ticker.h>

#include "esp_task_wdt.h"

// file system
#include "SPIFFS.h"

// magic number for update, if magic number is not equal to server's, then update
char MAGIC_NUMBER[10] = "HELL0";

bool isUpdate = false;

bool isSHOW = false;

bool reUpdate = false; // if update error, then reupdate

/*-------------------wifi--------------------------------------*/
void http_get_task();
void http_heartbeat();

const char *ssid = "508";           //"your ssid";
const char *password = "508508508"; //"your password";


// your server ip or domain name
String DOMIN = "192.168.1.119:8080";



#define EPD_WIDTH 600
#define EPD_HEIGHT 448

uint32_t IMG_SIZE = 0; // the img of download, some reason don't download  all the data.

const int LEDA = 2;

// WIFI_init(), new wifi and password
String USER_SSID = "Ymri";
String PASSWORD = "00000000";

// http_wifi_buffer
char temp_buffer[100];
const char *delimiter = ":";

String url = "http://" + DOMIN + "/epaper/Estatus/16?ip=";
// const Sring INIT_URL = "http://192.168.31.242:8080/epaper/Estatus/16?ip=";
const String HEART_URL = "http://" + DOMIN + "/epaper/Estatus/heartbeat/16";

String UPDATE_URL = "http://" + DOMIN + "/epaper/Estatus/bin/16";
// String UPDATE_URL = "http://192.168.1.119:8000/data.bin";
// ESP_LOG标签
static const char *TAG = "HTTP_CLIENT";

// hello handler for http
esp_err_t _http_event_handler(esp_http_client_event_t *evt)
{
    switch (evt->event_id)
    {
    case HTTP_EVENT_ERROR:
        ESP_LOGI(TAG, "HTTP_EVENT_ERROR");
        break;
    case HTTP_EVENT_ON_CONNECTED:
        ESP_LOGI(TAG, "HTTP_EVENT_ON_CONNECTED");
        break;
    case HTTP_EVENT_HEADER_SENT:
        ESP_LOGI(TAG, "HTTP_EVENT_HEADER_SENT");
        break;
    case HTTP_EVENT_ON_HEADER:
        ESP_LOGI(TAG, "HTTP_EVENT_ON_HEADER, key=%s, value=%s", evt->header_key, evt->header_value);
        break;
    case HTTP_EVENT_ON_DATA:
        ESP_LOGI(TAG, "HTTP_EVENT_ON_DATA, len=%d", evt->data_len);
        if (!esp_http_client_is_chunked_response(evt->client))
        {
            if (evt->data_len > 0)
            {
                // get userSetting from server
                memcpy(temp_buffer, evt->data, evt->data_len);
                Serial.println(temp_buffer);
                char *temp_ssid = strtok(temp_buffer, delimiter);
                char *temp_password = strtok(NULL, delimiter);
                USER_SSID = String(temp_ssid);
                PASSWORD = String(temp_password);
                Serial.println(USER_SSID);
                Serial.print(PASSWORD);
            }
        }
        break;
    case HTTP_EVENT_ON_FINISH:
        ESP_LOGI(TAG, "HTTP_EVENT_ON_FINISH");
        break;
    case HTTP_EVENT_DISCONNECTED:
        ESP_LOGI(TAG, "HTTP_EVENT_DISCONNECTED");
        break;
    }
    return ESP_OK;
}

//  handler for heartbeat
esp_err_t _http_event_handler_heart(esp_http_client_event_t *evt)
{
    switch (evt->event_id)
    {
    case HTTP_EVENT_ERROR:
        ESP_LOGI(TAG, "HTTP_EVENT_ERROR");
        break;
    case HTTP_EVENT_ON_CONNECTED:
        ESP_LOGI(TAG, "HTTP_EVENT_ON_CONNECTED");
        break;
    case HTTP_EVENT_HEADER_SENT:
        ESP_LOGI(TAG, "HTTP_EVENT_HEADER_SENT");
        break;
    case HTTP_EVENT_ON_HEADER:
        ESP_LOGI(TAG, "HTTP_EVENT_ON_HEADER, key=%s, value=%s", evt->header_key, evt->header_value);
        break;
    case HTTP_EVENT_ON_DATA:
        ESP_LOGI(TAG, "HTTP_EVENT_ON_DATA, len=%d", evt->data_len);
        if (!esp_http_client_is_chunked_response(evt->client))
        {
            if (evt->data_len > 0)
            {
                // get userSetting from server
                Serial.println(" get magic num ....");
                memcpy(temp_buffer, evt->data, evt->data_len);
                Serial.println(temp_buffer);
                bool flag = false;
                for (int i = 0; i < 4; i++)
                {
                    if ((!flag) && temp_buffer[i] != MAGIC_NUMBER[i])
                    {
                        isUpdate = true;
                        flag = true;
                        break;
                    }
                }
                if (isUpdate)
                {
                    memcpy(MAGIC_NUMBER, temp_buffer, 4 * sizeof(char));
                }
            }
        }
        break;
    case HTTP_EVENT_ON_FINISH:
        ESP_LOGI(TAG, "HTTP_EVENT_ON_FINISH");
        break;
    case HTTP_EVENT_DISCONNECTED:
        ESP_LOGI(TAG, "HTTP_EVENT_DISCONNECTED");
        break;
    }
    return ESP_OK;
}

char TIME_LOCAL_response_buffer[2048] = {0};

esp_http_client_config_t TIME_CONFIG;

esp_http_client_handle_t TIME_CLIENT;

// get Usersetting
void http_get_task()
{
    char local_response_buffer[2048] = {0};
    // String temp =
    esp_http_client_config_t config = {
        .url = url.c_str(),
        .event_handler = _http_event_handler,
    };
    TIME_CONFIG = {
        .url = url.c_str()};
    esp_http_client_handle_t client = esp_http_client_init(&config);
    TIME_CLIENT = esp_http_client_init(&TIME_CONFIG);
    esp_err_t err = esp_http_client_perform(client);

    if (err == ESP_OK)
    {
        ESP_LOGI(TAG, "HTTP GET Status = %d, content_length = %d",
                 esp_http_client_get_status_code(client),
                 esp_http_client_get_content_length(client));
    }
    else
    {
        ESP_LOGE(TAG, "HTTP GET request failed: %s", esp_err_to_name(err));
    }
    esp_http_client_cleanup(client);

    return;
}

/**test network */
void http_heartbeat()
{
    char local_response_buffer[2048] = {0};

    // char* tempurl = strcat(temp.c_str(),msg);
    esp_http_client_config_t config = {
        .url = HEART_URL.c_str(),
        .event_handler = _http_event_handler_heart,
    };
    Serial.println(" send heartbeat....");
    esp_http_client_handle_t client = esp_http_client_init(&config);
    // 执行GET请求
    esp_err_t err = esp_http_client_perform(client);

    if (err == ESP_OK)
    {
        ESP_LOGI(TAG, "HTTP GET Status = %d, content_length = %d",
                 esp_http_client_get_status_code(client),
                 esp_http_client_get_content_length(client));
    }
    else
    {
        ESP_LOGE(TAG, "HTTP GET request failed: %s", esp_err_to_name(err));
    }
    esp_http_client_cleanup(client);
}

/*-------------------wifi end--------------------------------------*/

/*-------------------epaper function--------------------------------------*/
/******************************************************************************
function :	send data
parameter:
    Data : Write data
******************************************************************************/
void EPD_5IN65F_SendCommand(UBYTE Reg)
{
    DEV_Digital_Write(EPD_DC_PIN, 0);
    DEV_Digital_Write(EPD_CS_PIN, 0);
    DEV_SPI_WriteByte(Reg);
    DEV_Digital_Write(EPD_CS_PIN, 1);
}

void EPD_5IN65F_SendData(UBYTE Data)
{
    DEV_Digital_Write(EPD_DC_PIN, 1);
    DEV_Digital_Write(EPD_CS_PIN, 0);
    DEV_SPI_WriteByte(Data);
    DEV_Digital_Write(EPD_CS_PIN, 1);
}

void EPD_5IN65F_BusyHigh(void) // If BUSYN=0 then waiting
{
    while (!(DEV_Digital_Read(EPD_BUSY_PIN)))
        ;
}

void EPD_5IN65F_BusyLow(void) // If BUSYN=1 then waiting
{
    while (DEV_Digital_Read(EPD_BUSY_PIN))
        ;
}

/*-------------------epaper function end --------------------------------------*/

/**
 * init Wifi and get UserSetting（wifi and password）
 *
 */
void initConfig()
{

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    // Applying SSID and password
    WiFi.begin(ssid, password);
    pinMode(2, OUTPUT);
    // digitalWrite
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    digitalWrite(LEDA, HIGH);
    Serial.println("");
    Serial.println("WiFi connected");
    String ip = WiFi.localIP().toString();
    url = url + ip;
    // get UserSetting
    http_get_task();
    Serial.println(USER_SSID);
    // if ssid is change ,reconnect wifi
    if (USER_SSID != "Ymrimini")
    {
        Serial.println("Disconnect and reconnect...");
        WiFi.disconnect();
        WiFi.begin(USER_SSID.c_str(), PASSWORD.c_str());
        int flag = 0;
        while (WiFi.status() != WL_CONNECTED)
        {
            delay(500);
            Serial.print(".");
            if (flag == 0)
            {
                digitalWrite(LEDA, LOW);
                flag = 1;
            }
            else
            {
                digitalWrite(LEDA, HIGH);
                flag = 0;
            }
        }
        // Reconnected success set LED to high
        digitalWrite(LEDA, HIGH);
        Serial.println("WiFi Reconnected success!");
    }
}

/**
 * Download file
 */
void downloadAndSaveFile(String fileName, String url)
{
    if (!SPIFFS.begin(true))
    {
        Serial.println("An Error has occurred while mounting SPIFFS");
        return;
    }
    Serial.println("begin download file");
    HTTPClient http;
    http.begin(url);
    int httpCode = http.GET();
    if (httpCode > 0)
    {
        // save file
        File file = SPIFFS.open(fileName, FILE_WRITE);
        // file found at server
        u_int32_t have_read = 0;
        uint8_t flag = 0;
        if (httpCode == HTTP_CODE_OK)
        {
            int len = http.getSize();
            int buff_size = 8128;
            unsigned char *buff = (unsigned char *)malloc(buff_size);
            WiFiClient *stream = http.getStreamPtr();
            while (http.connected() && (len > 0 || len == -1))
            {
                // Available limited to 16328 bytes. Might be TLS segementation.
                size_t size = stream->available();
                if (size)
                {
                    int c = stream->readBytes(buff, ((size > buff_size) ? buff_size : size));
                    file.write(buff, c);
                    if (len > 0)
                    {
                        len -= c;
                    }
                }
                delay(1);
            }
            file.close();
            free(buff);
        }
    }
    Serial.println("download success");
    http.end();
    delay(1500);
}
// for epaper read data
unsigned char buf[EPD_5IN65F_WIDTH];

/**
 * load data from file
 *  position sizeof(unsigned char)
 */
int readDataFromPosition(uint32_t position, u_int32_t length)
{
    File file = SPIFFS.open("/data.bin", FILE_READ);

    if (!file)
    {
        Serial.println("Failed to open file for reading");
        reUpdate = true;
        return 0;
    }
    // 跳转到指定位置
    if (file.seek(position * sizeof(unsigned char)))
    {
        // 创建一个缓存数组存放读取的数据
        int bytesRead = file.read(buf, length * sizeof(unsigned char)); // 从文件中读取数据
        return 1;
    }
    else
    {
        Serial.println("Failed to seek to position");
        reUpdate = true;
        return 0;
    }
    file.close();
    return 1;
}

void loadDataBin()
{
    DEV_Module_Init();
    EPD_5IN65F_Init();

    DEV_Delay_ms(100);
    // printf("e-Paper Init and Clear...\r\n");
    Serial.println("begin to show....");
    Paint_SetScale(7);
    UWORD i = 0, j = 0;
    EPD_5IN65F_SendCommand(0x61); // Set Resolution setting
    EPD_5IN65F_SendData(0x02);
    EPD_5IN65F_SendData(0x58);
    EPD_5IN65F_SendData(0x01);
    EPD_5IN65F_SendData(0xC0);
    EPD_5IN65F_SendCommand(0x10);
    for (i = 0; i < EPD_HEIGHT; i++)
    {
        readDataFromPosition(i * EPD_WIDTH / 2, EPD_WIDTH / 2);
        if (reUpdate)
        {
            break;
        }
        for (j = 0; j < EPD_WIDTH / 2; j++)
        {
            EPD_5IN65F_SendData(buf[j]);
        }
    }

    EPD_5IN65F_SendCommand(0x04); // 0x04
    EPD_5IN65F_BusyHigh();
    EPD_5IN65F_SendCommand(0x12); // 0x12
    EPD_5IN65F_BusyHigh();
    EPD_5IN65F_SendCommand(0x02); // 0x02
    EPD_5IN65F_BusyLow();
    DEV_Delay_ms(200);
    EPD_5IN65F_Sleep();
    Serial.println("End to show....");
    if (reUpdate)
    {
        // find error update and reset the flag
        reUpdate = false;
        isUpdate = false;
        isSHOW = false;
        // reset magic number
        MAGIC_NUMBER[0] = 'H';
        MAGIC_NUMBER[1] = 'E';
        MAGIC_NUMBER[2] = 'L';
        MAGIC_NUMBER[3] = 'L';
    }
}
void cleanData()
{
    SPIFFS.remove("/data.bin");
}
void setup()
{
    Serial.begin(115200);
    printf("init free_heap_size = %d\n", esp_get_free_heap_size());
    initConfig();
    // first update
    http_heartbeat();
    if (isUpdate)
    {
        downloadAndSaveFile("/data.bin", UPDATE_URL);
        esp_task_wdt_reset();
        loadDataBin();
        cleanData();
        isUpdate = false;
        isUpdate = false;
        isSHOW = false;
    }
    printf("after setup free_heap_size = %d\n", esp_get_free_heap_size());
}

/* The main loop -------------------------------------------------------------*/
void loop()
{
    if (!isUpdate)
    {
        Serial.println("begin to heartbeat....");
        http_heartbeat();
    }
    if (isUpdate && !isSHOW)
    {
        Serial.println("begin to refresh....");
        downloadAndSaveFile("/data.bin", UPDATE_URL);
        isSHOW = true;
    }
    if (isUpdate && isSHOW)
    {
        Serial.println("begin to show....");
        loadDataBin();
        cleanData();
        isUpdate = false;
        isUpdate = false;
        isSHOW = false;
    }
    printf("after loop free_heap_size = %d\n", esp_get_free_heap_size());
    // 30 seconds to check the update
    delay(10000);
}
