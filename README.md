#### Описание проекта:
Проект написан на языке python с использованием библиотеки tkinter.  
В проекте реализован криптографический протокол ecdsa с возможностью тестирования от лица двух пользователей (Alice и Bob).  
Также в проекте есть возможность работать с простыми числами.  
Простые числа можно генерировать случайным образом или вводить вручную, есть возможность для проверки числа на простоту с помощью метода пробных делений и теста Миллера-Рабина.

#### Для запуска проекта:
```python .\main.py```

#### Для сборки проект в .exe:
```pip install pyinstaller```  
```pyinstaller --onefile --windowed main.py```