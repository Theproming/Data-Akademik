from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="akademik_kampus"
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get total number of students
    cursor.execute("SELECT COUNT(*) FROM mahasiswa")
    total_students = cursor.fetchone()[0]

    # Get highest score
    cursor.execute("SELECT MAX(nilai_num) FROM mahasiswa")
    highest_score = cursor.fetchone()[0]

    # Get gender statistics
    cursor.execute("SELECT gender, COUNT(*) FROM mahasiswa GROUP BY gender")
    gender_stats = dict(cursor.fetchall())

    # Get course statistics
    cursor.execute("""
    SELECT mk.nama_matkul, COUNT(*) 
    FROM mahasiswa m
    JOIN mata_kuliah mk ON m.matkul_id = mk.id
    GROUP BY mk.nama_matkul
    """)
    course_stats = dict(cursor.fetchall())

    cursor.close()
    conn.close()

    return render_template('index.html', 
                           total_students=total_students,
                           highest_score=highest_score,
                           male_students=gender_stats.get('L', 0),
                           female_students=gender_stats.get('P', 0),
                           course_stats=course_stats)

@app.route('/data_entry_form')
def data_entry_form():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama_matkul FROM mata_kuliah")
    matkul_list = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template('data_entry_form.html', matkul_list=matkul_list)

@app.route('/submit_data_entry', methods=['POST'])
def submit_data_entry():
    nama = request.form['nama'].replace('0', 'O')
    nim = request.form['nim']
    matkul = request.form['matkul']
    gender = request.form['gender']
    nilai_num = int(request.form['nilai'])

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM mata_kuliah WHERE nama_matkul = %s", (matkul,))
    matkul_id = cursor.fetchone()[0]

    nilai_huruf = konversi_nilai(nilai_num)
    keterangan = "Lulus" if nilai_num >= 75 else "Remedial"

    query = """
    INSERT INTO mahasiswa (nama, nim, matkul_id, gender, nilai_num, nilai_huruf, keterangan)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (nama, nim, matkul_id, gender, nilai_num, nilai_huruf, keterangan)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Data berhasil ditambahkan!"})

@app.route('/data_display')
def data_display():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT m.nama, m.nim, mk.nama_matkul, m.gender, m.nilai_num, m.nilai_huruf, m.keterangan 
    FROM mahasiswa m
    JOIN mata_kuliah mk ON m.matkul_id = mk.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('data_display.html', data=data)

@app.route('/matkul_management')
def matkul_management():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama_matkul FROM mata_kuliah")
    matkul_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('matkul_management.html', matkul_list=matkul_list)

@app.route('/submit_matkul', methods=['POST'])
def submit_matkul():
    matkul = request.form['matkul']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mata_kuliah (nama_matkul) VALUES (%s)", (matkul,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Mata kuliah berhasil ditambahkan!"})

@app.route('/delete_matkul/<int:matkul_id>', methods=['DELETE'])
def delete_matkul(matkul_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mata_kuliah WHERE id = %s", (matkul_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Mata kuliah berhasil dihapus!"})

def konversi_nilai(nilai_num):
    if 80 <= nilai_num <= 100:
        return 'A'
    elif 60 <= nilai_num < 80:
        return 'B'
    elif 40 <= nilai_num < 60:
        return 'C'
    elif 20 <= nilai_num < 40:
        return 'D'
    else:
        return 'E'

if __name__ == '__main__':
    app.run(debug=True) 