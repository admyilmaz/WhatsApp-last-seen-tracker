from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# WebDriver'ı başlat
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")
print("QR kodunu tarayın ve devam edin...")

# Hedef kişinin adını veya numarasını belirleyin
target_name = "+905000000000  # WhatsApp'da kayıtlı olduğu şekilde girin

# WhatsApp Web'in yüklenmesini bekle
input("QR kodunu taradıktan sonra Enter'a basın...")

# Hedef kişinin sohbetine git
search_box = WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
)
search_box.click()
search_box.send_keys(target_name + Keys.ENTER)

# Online durumunu takip et ve kaydet
is_online = False
online_start_time = None

with open("whatsapp_online_log.txt", "a", encoding="utf-8") as log_file:
    log_file.write("Tarih ve Saat - Çevrimiçi Süresi\n")
    log_file.write("=" * 40 + "\n")

    try:
        while True:
            try:
                # Online durumunu kontrol et
                status = driver.find_element(By.XPATH, "//span[@title='çevrimiçi']")
                if not is_online:
                    # Çevrimiçi durumu yeni başladı
                    is_online = True
                    online_start_time = datetime.now()
                    print(f"{online_start_time.strftime('%Y-%m-%d %H:%M:%S')} - Çevrimiçi oldu")
            except:
                if is_online:
                    # Çevrimiçi durumu sona erdi
                    is_online = False
                    online_end_time = datetime.now()
                    online_duration = online_end_time - online_start_time
                    print(f"{online_end_time.strftime('%Y-%m-%d %H:%M:%S')} - Çevrimdışı oldu")
                    
                    # Çevrimiçi süresini kaydet
                    log_file.write(
                        f"{online_start_time.strftime('%Y-%m-%d %H:%M:%S')} - "
                        f"{online_end_time.strftime('%H:%M:%S')} | Süre: {online_duration}\n"
                    )
                    log_file.flush()

            # Her 5 saniyede bir kontrol et
            time.sleep(5)

    except KeyboardInterrupt:
        print("Takip sonlandırıldı.")
