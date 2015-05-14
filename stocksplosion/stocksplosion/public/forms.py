from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

class QuoteForm(Form):
  symbol = TextField('Symbol', validators=[DataRequired()])

  def __init__(self, *args, **kwargs):
    super(QuoteForm, self).__init__(*args, **kwargs)
