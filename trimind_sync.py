import sys, os
sys.path.insert(0, '/Users/josevictorfrancisco/Library/Python/3.9/lib/python/site-packages')
from garminconnect import Garmin
import datetime, urllib.request, json

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://rotzznmlcrqwtrxesezn.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvdHp6bm1sY3Jxd3RyeGVzZXpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkzODEwMTgsImV4cCI6MjA5NDk1NzAxOH0.rbGvnLTvWRmA-217TBplQXPTWHeZHUmkaeMk_BSfLp0")
USER_ID = "4385160f-c76f-4649-973f-fb0f8f92065b"
GARMIN_EMAIL = os.environ.get("GARMIN_EMAIL", "jvictorvf@hotmail.com")
GARMIN_PASSWORD = os.environ.get("GARMIN_PASSWORD", "Iglu45220052.")

def supabase_upsert(table, data, conflict_col="user_id,date"):
    url = f"{SUPABASE_URL}/rest/v1/{table}?on_conflict={conflict_col}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("apikey", SUPABASE_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Prefer", "resolution=merge-duplicates,return=minimal")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Supabase error: {e}")
        return False

def sync():
    today = datetime.date.today().isoformat()
    print(f"Sincronizando {today}...")
    api = Garmin(GARMIN_EMAIL, GARMIN_PASSWORD)
    api.login()
    print("Login OK!")
    metrics = {"user_id": USER_ID, "date": today}
    try:
        sleep = api.get_sleep_data(today)
        dto = sleep.get("dailySleepDTO", {})
        if dto.get("sleepTimeSeconds"): metrics["sleep_hours"] = round(dto["sleepTimeSeconds"]/3600,2)
        if dto.get("deepSleepSeconds"): metrics["sleep_deep_min"] = round(dto["deepSleepSeconds"]/60)
        if dto.get("lightSleepSeconds"): metrics["sleep_light_min"] = round(dto["lightSleepSeconds"]/60)
        if dto.get("remSleepSeconds"): metrics["sleep_rem_min"] = round(dto["remSleepSeconds"]/60)
        if dto.get("awakeSleepSeconds"): metrics["sleep_awake_min"] = round(dto["awakeSleepSeconds"]/60)
        scores = dto.get("sleepScores",{})
        if scores.get("overall",{}).get("value"): metrics["sleep_score"] = scores["overall"]["value"]
        elif dto.get("sleepScore"): metrics["sleep_score"] = dto["sleepScore"]
        print(f"Sono: {metrics.get('sleep_hours')}h Score:{metrics.get('sleep_score')}")
    except Exception as e: print(f"Sono erro: {e}")
    try:
        hrv = api.get_hrv_data(today)
        s = hrv.get("hrvSummary",{})
        val = s.get("lastNight") or s.get("weeklyAvg")
        if val: metrics["hrv_ms"] = val; print(f"HRV: {val}ms")
    except Exception as e: print(f"HRV erro: {e}")
    try:
        stress = api.get_stress_data(today)
        avg = stress.get("avgStressLevel")
        if avg and avg > 0: metrics["stress_avg"] = avg; print(f"Stress: {avg}")
    except Exception as e: print(f"Stress erro: {e}")
    try:
        rhr = api.get_rhr_day(today)
        val = rhr.get("restingHeartRate") or rhr.get("value")
        if val: metrics["resting_hr"] = val; print(f"FC repouso: {val}bpm")
    except Exception as e: print(f"FC erro: {e}")
    if supabase_upsert("daily_metrics", metrics):
        print(f"Salvo! {len(metrics)-2} metricas sincronizadas")
    else:
        print("Erro ao salvar")

if __name__ == "__main__":
    sync()
