#!/usr/bin/env python
# Yukarıdaki satır, bu dosyanın bir Python script'i olarak çalıştırılacağını belirtiyor.
# Ayrıca ROS ortamında çalıştırılması gerektiğini gösteriyor.

import rospy  # ROS için gerekli Python modülü
from geometry_msgs.msg import Twist  # Robot hareketlerini kontrol etmek için Twist mesajı
import sys, select, termios, tty  # Klavye girdilerini almak için kullanılan Python modülleri

def get_key():
    """
    Kullanıcıdan bir tuşa basıldığında bu fonksiyon o tuşu okur.
    """
    tty.setraw(sys.stdin.fileno())  # Terminali raw moda alır, böylece doğrudan tuş girişlerini okuyabiliriz.
    select.select([sys.stdin], [], [], 0.1)  # Tuş girdisi için 0.1 saniye bekler.
    key = sys.stdin.read(1)  # Tek bir tuşu okur.
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))  # Terminal ayarlarını eski haline getirir.
    return key  # Basılan tuşu döndürür.

def control_robot():
    """
    Robotu klavyeden kontrol etmek için ana fonksiyon.
    """
    rospy.init_node('keyboard_control')  # ROS Node'u başlatır ve ismini 'keyboard_control' olarak ayarlar.
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)  # /cmd_vel topic'ine Twist mesajları yayınlamak için bir publisher oluşturur.
    rate = rospy.Rate(10)  # Mesaj gönderme hızını 10 Hz olarak ayarlar.
    start_time = rospy.Time.now()  # Node'un başlama zamanını kaydeder.

    rospy.loginfo("Keyboard Control Node Initialized. Use W/A/S/D to move, Q to quit.")
    # Terminalde başlangıç mesajını gösterir.

    while not rospy.is_shutdown():  # Node kapatılana kadar döngüyü çalıştırır.
        elapsed_time = (rospy.Time.now() - start_time).to_sec()
        # Geçen süreyi hesaplar.

        if elapsed_time >= 60:
            # Eğer 60 saniye geçtiyse, robotu durdur ve döngüyü bitir.
            rospy.loginfo("Time limit reached. Stopping...")
            break

        key = get_key()  # Kullanıcıdan bir tuş girdisi alır.
        twist = Twist()  # Twist mesajı oluşturur.

        if key == 'w':  # Eğer 'w' tuşuna basıldıysa:
            twist.linear.x = 1.0  # İleri doğru hareket et.
            rospy.loginfo("Moving forward.")  # Terminalde bilgi göster.
        elif key == 's':  # Eğer 's' tuşuna basıldıysa:
            twist.linear.x = -1.0  # Geri doğru hareket et.
            rospy.loginfo("Moving backward.")  # Terminalde bilgi göster.
        elif key == 'a':  # Eğer 'a' tuşuna basıldıysa:
            twist.angular.z = 1.0  # Sola dön.
            rospy.loginfo("Turning left.")  # Terminalde bilgi göster.
        elif key == 'd':  # Eğer 'd' tuşuna basıldıysa:
            twist.angular.z = -1.0  # Sağa dön.
            rospy.loginfo("Turning right.")  # Terminalde bilgi göster.
        elif key == 'q':  # Eğer 'q' tuşuna basıldıysa:
            rospy.loginfo("Stopping the robot.")  # Terminalde bilgi göster.
            break  # Döngüyü bitir.

        pub.publish(twist)  # Hareket komutunu yayınla.
        rate.sleep()  # Bir sonraki döngüye kadar bekle.

    rospy.loginfo("Shutting down Keyboard Control Node.")
    # Node kapatıldığında terminale bilgi yazdırır.

if __name__ == '__main__':
    try:
        control_robot()  # Ana kontrol fonksiyonunu çalıştır.
    except rospy.ROSInterruptException:
        # Eğer bir ROS kesintisi olursa (örneğin Ctrl+C), hata vermeden çık.
        pass

