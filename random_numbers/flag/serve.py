from flask import Flask, render_template, flash, request
from contract_handler import ContractHandler
from wtforms import Form, IntegerField, validators, StringField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ValidationForm(Form):
    number = IntegerField('Number', [validators.NumberRange(min=1, max=30)])

@app.route("/", methods=['GET', 'POST'])
def index():

    try:
        contract = ContractHandler()
    except ValueError as err:
        flash(err)
        return render_template('base.html', form=form)

    form = ValidationForm(request.form)
    if request.method == 'POST' and form.validate():
        numberBet = request.form['number']
        print('*****\tThe user picked {}'.format(numberBet))

        contract.placeBet()
        winningNumber = contract.getWinningNumber()
        print('{0} == {1}'.format(numberBet, winningNumber))
        if int(winningNumber) == int(numberBet):
            flash('You found the winning number')
        else:
            flash('Please try again, winning number was {}'.format(winningNumber))

    return render_template('base.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="0.0.0.0", port=5000)
