REM C:\Python27\Scripts\pybabel -v extract -F babel.config -o ./translations/messages.pot ./

REM C:\Python27\Scripts\pybabel init -l en_US -d ./translations -i ./translations/messages.pot
REM C:\Python27\Scripts\pybabel init -l zh_CN -d ./translations -i ./translations/messages.pot

REM C:\Python27\Scripts\pybabel update -l en_US -d ./translations/ -i ./translations/messages.pot
REM C:\Python27\Scripts\pybabel update -l zh_CN -d ./translations/ -i ./translations/messages.pot

C:\Python27\Scripts\pybabel compile -f -d ./translations
