from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, session)
from urllib2 import urlopen, HTTPError
from datetime import timedelta, datetime
import json

from stocksplosion.public.forms import QuoteForm

blueprint = Blueprint('public', __name__, static_folder="../static")


_url_root = 'http://stocksplosion.apsis.io/api'
_date_format = '%Y%m%d'

_buy_slope = 1000
_sell_slope = -500

def slope_from_prices(prices):
  sorted_p = sorted(prices)
  slope = 0

  for i in range(0, len(sorted_p)):
    if i < len(sorted_p) - 1:
      first_date_str = sorted_p[i]
      second_date_str = sorted_p[i+1]
      first_value = prices[first_date_str]
      second_value = prices[second_date_str]

      first_date = datetime.strptime(first_date_str, _date_format)
      second_date = datetime.strptime(second_date_str, _date_format)

      value_d = second_value - first_value
      time_d = second_date - first_date

      slope += value_d /time_d.days

  return slope

def date_to_str(date):
  return date.strftime(_date_format)

def build_graph(quote):
  chartID = 'chart_id'
  chart_type = 'line'
  chart_height = 350

  prices = quote['prices']
  sort = sorted(prices)

  #TODO: this can be more Pythonic
  date_ordered = [i for i in sort]
  price_ordered = [prices[i] for i in sort]

  chart = {'renderTo': chartID, "type": chart_type, "height": chart_height}
  series = [{"name": quote['company']['symbol'], "data": price_ordered}]
  title = {"text": 'Performance'}
  xAxis = {"title": {"text": 'Price'}, 'categories': date_ordered}
  yAxis = {"title": {"text": 'Date'}}

  return {'chartID':chartID,
          'chart':chart,
          'series':series,
          'title':title,
          'xAxis':xAxis,
          'yAxis':yAxis}

@blueprint.route("/", methods=["GET", "POST"])
def home():
  quote = QuoteForm(request.form)

  missing = request.args.get('missing')

  if request.method == 'POST':
    return redirect(url_for('public.quote', symbol=quote.symbol.data))
  #TODO: auto complete from valid symbols. Reject missing symbols on this page
  return render_template("public/home.html", quote=quote, missing=missing)

@blueprint.route("/quote/<symbol>/", methods=["GET"])
def quote(symbol):
  #TODO: past days to search from config
  start_date = datetime.utcnow() + timedelta(days=-20)
  end_date = datetime.utcnow()

  start_date_str = date_to_str(start_date)
  end_date_str = date_to_str(end_date)

  url = '{root}/company/{symbol}?startdate={start}&enddate={end}'.format(
    root= _url_root, symbol=symbol, start=start_date_str, end=end_date_str)
  quote = None

  #Get info from stocksplosion
  try:
    quote_str = urlopen(url).read();
    quote = json.loads(quote_str)
  except HTTPError as e:
    return redirect(url_for('public.home', missing=True))

  slope = slope_from_prices(quote['prices'])

  #TODO: get slope from config
  recomendation = "Wait"
  if slope > _buy_slope:
    recomendation = "Buy"
  elif slope < _sell_slope:
    recomendation = "Sell"

  graph = build_graph(quote)

  return render_template("public/quote.html",
                         company_name=quote['company']['name'],
                         symbol=symbol,
                         graph=graph,
                         recomendation=recomendation)
