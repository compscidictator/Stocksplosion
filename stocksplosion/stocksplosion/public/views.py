from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, session)

from stocksplosion.public.forms import QuoteForm

blueprint = Blueprint('public', __name__, static_folder="../static")

@blueprint.route("/", methods=["GET", "POST"])
def home():
  quote = QuoteForm(request.form)

  if request.method == 'POST':
    return redirect(url_for('public.quote', symbol=quote.symbol.data))

  return render_template("public/home.html", quote=quote)

@blueprint.route("/quote/<symbol>/", methods=["GET"])
def quote(symbol):
  #Give recent pricing info
  #Buy/Sell/Wait recomendation
  return render_template("public/quote.html", symbol=symbol)
