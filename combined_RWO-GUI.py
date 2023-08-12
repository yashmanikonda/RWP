import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QCheckBox
from PyQt5 import Qt
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

def get_repository_links():
    # Wait for the repositories list to load
    repositories_list_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'user-repositories-list'))
    )

    # Find all anchor elements (links) within the div
    links = repositories_list_div.find_elements(By.TAG_NAME, 'a')

    # Extract and return the repository URLs
    return [link.get_attribute('href') for link in links]

class ErrorHandlingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Error Handling")
        self.setGeometry(400, 400, 300, 100)

        error_label = QLabel("Incorrect Username or Password")
        self.popup_button = QPushButton("close")

        layout = QVBoxLayout()
        layout.addWidget(error_label)
        self.setLayout(layout)


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RWO")
        self.setGeometry(500, 500, 300, 150)

        self.username_label = QLabel("GitHub Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("GitHub Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)


        self.login_button = QPushButton("Login")
        self.close_button = QPushButton("Exit")

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.login_button)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.login_button.clicked.connect(self.on_login)
        self.close_button.clicked.connect(self.close_app)

    def toggle_password_visibility(self, state):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)


    def on_login(self):
            username = self.username_input.text()
            password = self.password_input.text()

            driver.maximize_window()
            driver.get('https://github.com/login')

            authenticated = False

            try:
                username_element = driver.find_element(By.ID, 'login_field')
                username_element.clear()
                username_element.send_keys(username)

                password_element = driver.find_element(By.ID, 'password')
                password_element.clear()
                password_element.send_keys(password)

                sign_in_button = driver.find_element(By.CLASS_NAME, 'js-sign-in-button')
                sign_in_button.click()

                try:
                    error_message = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'js-flash-alert'))
                    )
                    error_popup = ErrorHandlingApp()
                    error_popup.show()

                except TimeoutException:
                    authenticated = True

                except NoSuchElementException:
                    authenticated = True
                    print("Login Successful")


                if authenticated:

                    self.layout().removeWidget(self.login_button)


                    profile_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, 'AppHeader-user'))
                    )
                    profile_button.click()

                    repo_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    f'//span[@data-view-component="true" and contains(@class, "ActionListItem-label") and contains(text(), "Your repositories")]'))
                    )
                    repo_button.click()


            finally:
                pass

    def close_app(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ErrorHandlingApp()
    window.show()
    sys.exit(app.exec_())
