from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Назва товару', validators=[
        DataRequired(message="Назва є обов'язковою"), 
        Length(min=3, message="Назва повинна містити мінімум 3 символи")
    ])
    
    content = TextAreaField('Опис товару', validators=[
        DataRequired(message="Опис є обов'язковим")
    ])
    
    price = DecimalField('Ціна', validators=[
        DataRequired(message="Ціна є обов'язковою"), 
        NumberRange(min=0.01, message="Ціна має бути додатнім числом")
    ], places=2)
    
    category = SelectField('Категорія', choices=[
        ('electronics', 'Електроніка'),
        ('clothing', 'Одяг'),
        ('books', 'Книги'),
        ('other', 'Інше')
    ], validators=[DataRequired()])
    
    quantity = IntegerField('Кількість', validators=[
        DataRequired(message="Кількість є обов'язковою"), 
        NumberRange(min=0, message="Кількість не може бути від'ємною")
    ])
    
    image = FileField('Зображення товару', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Дозволені лише файли форматів PNG, JPG, JPEG!')
    ])
    
    submit = SubmitField('Зберегти товар')