"""Test otomatis AI FAQ Chatbot - 8 test."""
from app import app, cari_jawaban

client = app.test_client()

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_home_ok():
    r = client.get("/")
    assert r.status_code == 200

def test_chat_jam_buka():
    r = client.post("/api/chat", json={"pertanyaan": "Jam buka klinik jam berapa?"})
    assert r.status_code == 200
    assert "08.00" in r.get_json()["jawaban"]

def test_chat_biaya():
    r = client.post("/api/chat", json={"pertanyaan": "Berapa biaya daftar pakai BPJS?"})
    assert r.status_code == 200
    assert "JKN" in r.get_json()["jawaban"]

def test_chat_kosong_ditolak():
    r = client.post("/api/chat", json={"pertanyaan": "   "})
    assert r.status_code == 400

def test_chat_tanpa_field_ditolak():
    r = client.post("/api/chat", json={})
    assert r.status_code == 400

def test_chat_bukan_json_ditolak():
    r = client.post("/api/chat", data="halo")
    assert r.status_code == 400

def test_cari_jawaban_default():
    assert "belum mengerti" in cari_jawaban("xyzqqq tidak jelas")
