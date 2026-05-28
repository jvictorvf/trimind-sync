import sys, os
sys.path.insert(0, '/Users/josevictorfrancisco/Library/Python/3.9/lib/python/site-packages')
from garminconnect import Garmin
import datetime, urllib.request, json

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://rotzznmlcrqwtrxesezn.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvdHp6bm1sY3Jxd3RyeGVzZXpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkzODEwMTgsImV4cCI6MjA5NDk1NzAxOH0.rbGvnLTvWRmA-217TBplQXPTWHeZHUmkaeMk_BSfLp0")
USER_ID = "4385160f-c76f-4649-973f-fb0f8f92065b"
GARMIN_EMAIL = os.environ.get("GARMIN_EMAIL", "jvictorvf@hotmail.com")
GARMIN_PASSWORD = os.environ.get("GARMIN_PASSWORD", "Iglu45220052.")

# Fuso horário Brasília = UTC-3
def today_brazil():
    return (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).date().isoformat()

def yesterday_brazil():
    return (datetime.datetime.utcnow() - datetime.timedelta(hours=3) - datetime.timedelta(days=1)).date().isoformat()

SKIP_TYPES = {"virtual_ride", "e_bike_fitness", "other"}
SPORT_MAP = {
    "running": "run", "trail_running": "run", "treadmill_running": "run",
    "cycling": "bike", "indoor_cycling": "bike", "mountain_biking": "bike",
    "swimming": "swim", "open_water_swimming": "swim", "lap_swimming": "swim", "pool_swimming": "swim",
    "strength_training": "strength", "fitness_equipment": "strength",
}

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

def check_exists(sport, date):
    url = f"{SUPABASE_URL}/rest/v1/workouts?user_id=eq.{USER_ID}&date=eq.{date}&sport=eq.{sport}&select=id"
    req = urllib.request.Request(url)
    req.add_header("apikey", SUPABASE_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
    try:
        return len(json.loads(urllib.request.urlopen(req).read())) > 0
    except:
        return False

def sync_activities(api, today, yesterday):
    try:
        activities = api.get_activities_by_date(yesterday, today)
        if not activities:
            print("Nenhuma atividade encontrada")
            return
        saved = 0
        saved_sports_by_date = {}
        for act in activities:
            act_type = act.get("activityType", {}).get("typeKey", "other")
            if act_type in SKIP_TYPES:
                print(f"Ignorando: {act.get('activityName')} ({act_type})")
                continue
            sport = SPORT_MAP.get(act_type)
            if not sport:
                print(f"Tipo ignorado: {act_type}")
                continue
            start_time = act.get("startTimeLocal", "")
            date = start_time[:10] if start_time else yesterday
            # Evitar duplicata de mesmo sport no mesmo dia
            key = f"{sport}_{date}"
            if key in saved_sports_by_date:
                print(f"Duplicata ignorada: {sport} {date}")
                continue
            if check_exists(sport, date):
                print(f"Ja existe: {sport} {date} — pulando")
                saved_sports_by_date[key] = True
                continue
            dur_s = int(act.get("duration", 0))
            dist_m = int(act.get("distance", 0))
            avg_hr = act.get("averageHR")
            max_hr = act.get("maxHR")
            avg_power = act.get("avgPower")
            avg_speed = act.get("averageSpeed")
            avg_speed_kmh = round(avg_speed * 3.6, 1) if avg_speed else None
            tss_garmin = act.get("trainingStressScore") or None
            workout = {
                "user_id": USER_ID, "date": date, "sport": sport,
                "title": act.get("activityName", sport.upper()),
                "status": "completed",
                "actual_duration_s": dur_s, "actual_distance_m": dist_m,
            }
            if avg_hr: workout["avg_hr"] = int(avg_hr)
            if max_hr: workout["max_hr"] = int(max_hr)
            if avg_power: workout["avg_power_watts"] = int(avg_power)
            if avg_speed_kmh: workout["avg_speed_kmh"] = avg_speed_kmh
            if tss_garmin: workout["tss_actual"] = float(tss_garmin)
            ins_req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/workouts", data=json.dumps(workout).encode(), method="POST")
            ins_req.add_header("apikey", SUPABASE_KEY)
            ins_req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
            ins_req.add_header("Content-Type", "application/json")
            ins_req.add_header("Prefer", "return=minimal")
            try:
                urllib.request.urlopen(ins_req)
                print(f"Treino salvo: {sport} {date} {dur_s//60}min FC:{int(avg_hr) if avg_hr else '?'}bpm")
                saved += 1
                saved_sports_by_date[key] = True
            except Exception as e:
                print(f"Erro ao salvar treino: {e}")
        print(f"{saved} treino(s) novo(s) sincronizado(s)")
    except Exception as e:
        print(f"Atividades erro: {e}")

def sync():
    today = today_brazil()
    yesterday = yesterday_brazil()
    print(f"Sincronizando {today} (Brasilia)...")
    api = Garmin(GARMIN_EMAIL, GARMIN_PASSWORD)
    api.login()
    print("Login OK!")
    metrics = {"user_id": USER_ID, "date": today}
    try:
        sleep = api.get_sleep_data(today)
        dto = sleep.get("dailySleepDTO", {})
        if dto.get("sleepTimeSeconds"): metrics["sleep_hours"] = round(dto["sleepTimeSeconds"]/3600, 2)
        if dto.get("deepSleepSeconds"): metrics["sleep_deep_min"] = round(dto["deepSleepSeconds"]/60)
        if dto.get("lightSleepSeconds"): metrics["sleep_light_min"] = round(dto["lightSleepSeconds"]/60)
        if dto.get("remSleepSeconds"): metrics["sleep_rem_min"] = round(dto["remSleepSeconds"]/60)
        if dto.get("awakeSleepSeconds"): metrics["sleep_awake_min"] = round(dto["awakeSleepSeconds"]/60)
        scores = dto.get("sleepScores", {})
        if scores.get("overall", {}).get("value"): metrics["sleep_score"] = scores["overall"]["value"]
        elif dto.get("sleepScore"): metrics["sleep_score"] = dto["sleepScore"]
        print(f"Sono: {metrics.get('sleep_hours')}h Score:{metrics.get('sleep_score')}")
    except Exception as e: print(f"Sono erro: {e}")
    try:
        hrv = api.get_hrv_data(today)
        s = hrv.get("hrvSummary", {})
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
    sync_activities(api, today, yesterday)

if __name__ == "__main__":
    sync()
