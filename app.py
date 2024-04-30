from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'hotel.db'

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

class Hotel:
    def get_rooms(self):
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM rooms')
        rooms = c.fetchall()
        conn.close()
        return rooms

    def check_in(self, room_no, guests):
        conn = get_db()
        c = conn.cursor()
        c.execute('UPDATE rooms SET occupied = 1, guests = ? WHERE room_no = ?', (', '.join(guests), room_no))
        conn.commit()
        conn.close()

    def check_out(self, room_no):
        conn = get_db()
        c = conn.cursor()
        c.execute('UPDATE rooms SET occupied = 0, guests = NULL WHERE room_no = ?', (room_no,))
        conn.commit()
        conn.close()

    def add_room(self, room_no, capacity, rate):
        conn = get_db()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO rooms (room_no, capacity, rate) VALUES (?, ?, ?)', (room_no, capacity, rate))
            conn.commit()
        except sqlite3.IntegrityError:
            return False
        conn.close()
        return True

hotel = Hotel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    rooms = hotel.get_rooms()
    return render_template('rooms.html', hotel=hotel, rooms=rooms)

@app.route('/book_rooms')
def book_rooms():
    return render_template('book_rooms.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/check_in', methods=['POST'])
def check_in():
    room_no = int(request.form['room_no'])
    guests = request.form['guests'].split(',')
    hotel.check_in(room_no, guests)
    return redirect(url_for('rooms'))

@app.route('/check_out', methods=['POST'])
def check_out():
    room_no = int(request.form['room_no'])
    hotel.check_out(room_no)
    return redirect(url_for('rooms'))

@app.route('/add_room', methods=['POST'])
def add_room():
    room_no = int(request.form['room_no'])
    capacity = int(request.form['capacity'])
    rate = float(request.form['rate'])
    if hotel.add_room(room_no, capacity, rate):
        return redirect(url_for('rooms'))
    else:
        return render_template('error.html', message='Room number already exists')

@app.route('/show_data')
def show_data():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM rooms')
    rows = c.fetchall()
    conn.close()
    return render_template('show_data.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)