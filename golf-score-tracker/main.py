from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

holes = [
    {"hole": 1, "par": 5, "yardage": 545, "lat": 32.5615, "lng": -84.8727},
    {"hole": 2, "par": 4, "yardage": 340, "lat": 32.5616, "lng": -84.8728},
    {"hole": 3, "par": 3, "yardage": 170, "lat": 32.5617, "lng": -84.8729},
    {"hole": 4, "par": 5, "yardage": 535, "lat": 32.5618, "lng": -84.8730},
    {"hole": 5, "par": 3, "yardage": 173, "lat": 32.5619, "lng": -84.8731},
    {"hole": 6, "par": 4, "yardage": 440, "lat": 32.5620, "lng": -84.8732},
    {"hole": 7, "par": 4, "yardage": 375, "lat": 32.5621, "lng": -84.8733},
    {"hole": 8, "par": 4, "yardage": 387, "lat": 32.5622, "lng": -84.8734},
    {"hole": 9, "par": 4, "yardage": 415, "lat": 32.5623, "lng": -84.8735},
    {"hole": 10, "par": 4, "yardage": 385, "lat": 32.5624, "lng": -84.8736},
    {"hole": 11, "par": 5, "yardage": 515, "lat": 32.5625, "lng": -84.8737},
    {"hole": 12, "par": 4, "yardage": 420, "lat": 32.5626, "lng": -84.8738},
    {"hole": 13, "par": 4, "yardage": 360, "lat": 32.5627, "lng": -84.8739},
    {"hole": 14, "par": 3, "yardage": 145, "lat": 32.5628, "lng": -84.8740},
    {"hole": 15, "par": 4, "yardage": 390, "lat": 32.5629, "lng": -84.8741},
    {"hole": 16, "par": 5, "yardage": 525, "lat": 32.5630, "lng": -84.8742},
    {"hole": 17, "par": 3, "yardage": 150, "lat": 32.5631, "lng": -84.8743},
    {"hole": 18, "par": 4, "yardage": 435, "lat": 32.5632, "lng": -84.8744}
]

@app.route('/', methods=['GET', 'POST'])
def player_names():
    if request.method == 'POST':
        players = [p.strip() for p in request.form['players'].split(',') if p.strip()]
        session['players'] = players
        session['scores'] = {player: [] for player in players}
        session['current_hole'] = 1
        return redirect(url_for('hole_score', hole_number=1))
    return render_template('player_names.html')

@app.route('/hole/<int:hole_number>', methods=['GET', 'POST'])
def hole_score(hole_number):
    players = session.get('players')
    scores = session.get('scores')
    if not players or not scores:
        return redirect(url_for('player_names'))
    if request.method == 'POST':
        for player in players:
            score = int(request.form.get(f'score_{player}', 0))
            scores[player].append(score)
        session['scores'] = scores
        if hole_number < 18:
            return redirect(url_for('hole_score', hole_number=hole_number+1))
        else:
            return redirect(url_for('results'))
    hole = holes[hole_number-1]
    return render_template('hole_score.html', hole=hole, players=players, hole_number=hole_number)

@app.route('/results')
def results():
    players = session.get('players')
    scores = session.get('scores')
    if not players or not scores:
        return redirect(url_for('player_names'))
    totals = {player: sum(scores[player]) for player in players}
    winner = min(totals, key=totals.get)
    return render_template('results.html', totals=totals, winner=winner)

if __name__ == '__main__':
    app.run(debug=True)