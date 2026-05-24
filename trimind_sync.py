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





def sync_trainingpeaks():
    import datetime, urllib.request, json, urllib.parse
    
    TP_COOKIE = "Production_tpAuth=V001aheYPkwmKUmw75FR4_utn_e8GPafFLnjYbL212ZOIGtAToHIO0BarKJ9NdVazjlDi8TVSEscv1o-Pq7tNReQZsost2oCu_vB21QgDf6EB4Dph2LB3qKgk6po9yR8w4J8wU0ZP6-4qxgUGfHNRr171SIcBcxQ3pvwaiv4fHvCK6rbXnSuH3fJ6atZvEha_KojBcGBfCSI5q-uxWEZUoSrYnhN6_gVTcjVHcC21AIQccfVEx3YWzQiy8zYI2Anf5zAyeCWnx_TQ_uKzf0g7VBBy7J83p12Ks2lUeEpVPLjQVZuSytAp4056HH2_8ZVDP-2KN3CaxS-eCi1EqyWsOcYG1WH2pQ-fB2dC7x8ZVeY3t1h4eeSLzrl8xAqdKEP9q1OTXx3j0lcFSJl-E-oBOMQGNiAmVcMikejnwQjBYMd9JH5xcH4gdvek4kXkeL7esaUsoxGGa8tO9ZEiIA0q_B0nsKXxMaCpvvxugotaJggNpl0gtVdDegmml9wcFrw1eKMEMLxP6hm4ooq8gpT-BHfzkX2ACh3kCHstWPk-zTXp0g1-aGIEKKIhr4Sur4dTNAIQMPw69uxPC6ChLMiw9RX5GldWoqHFZqeIulaL7ZmUmC9gBgIHfMVJevBqFYc1u1eWUetP5egNlYuYHVqRFGdA3yv5PKBAlUtvMsK3dQIezVHXQPx_chFyrYG5G2DV4WOeU0JmMuM1YOchlv5nfzukFQHJeilELy06nWDFs_JxjpREjUGYrVj539Rrzc4ifYryX34c6pqRFabCm3SXI2f6lhanpkl8N-16z8kfSv7aIJFCXTCu0B6TxMrS8spCKR4NrPvG5m9byBOfcfir_5C_u6jOaT0A3VAXk7kz4gAhpLcs89Ce8yf-vrW5v1kl7KQalqSs_-4z8xCnZ8xDIzTiDEp-F4Rd6zBOHSzh0bcQyzAnLAXeLFkWLaYXFlIm0AkNVZe3fvBCTKADHWMcpMPEEDRXSxaq4v2ZOYF0Gb_bq9Vg7EmLqvgPNG23V3aP_CBD7Yv5eFToufrhS7_JEtPZEkq2nKzI4aPXfdhqlJ8a-63Rdc846uR3ecuvx4ATTMt6JKrmwXyDXSoBlc0atVWy4PQQd6TbpvuPNHQF3p40Y8HZ_88G-nl5ZqYqVFY2d6Ano-E7obBuN6uTBDz7_2a1pkY8-XicuppmD9pjZNJfjOJBQsR3Xm1GDCYLady5w8N4B_cPp2oSacgcF4_kW4b57auc8UeH-xoki9wpFpFoGG7yXhlgYx0d3WUe1txRgySP7W2lOAOzoCAQh4KwitwJ2L3iNEl0ocWcZ1KewOeR7izQ22IljiCWk8huiTmVsCz0aEOHU56DA-hLb_QvHM2nuqNFKrW4ResEdf2mJ-kHddSyyCmpTUnLHj7JyHsMHm3PCIgPFI-ioVBurqCrQw5SNeBSKxuTarkTrkmlGdVszp04MLekXQG5hFuy8kXB8OzBbtF7534U_hBH5Hd75HVa8m1P6b2DAmNBNCd6Z3BWLml8yvBAWQIaWa5uOyu2PmW9qdfBwxTJhIC-mhGqKNPjo2TifjVmfOYO4kdEUHbdzqyOssg46Xg44Ck0PBrVr3VHsYH4hPI2m2h0-2mdUjMYKkaPXGGeHIClwQ1z22V0Fzu4_1eRtaPqAFtfUW3uX-LoIpaNNLnwrUjB63i9FQ83hFD8YjeaFVy_8ts11uyQYGD0sMwjwHx_suNa9rny-Gdse4Hrd5Ovt-wojAVy_sQR-uVMHDnaXmdRSlDb_TOoTs1"
    
    today = datetime.date.today()
    start = today.isoformat()
    end = (today + datetime.timedelta(days=14)).isoformat()
    
    def tp_get(path):
        url = f"https://tpapi.trainingpeaks.com{path}"
        req = urllib.request.Request(url)
        req.add_header("Cookie", TP_COOKIE)
        req.add_header("User-Agent", "Mozilla/5.0")
        req.add_header("Accept", "application/json")
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            return json.loads(resp.read())
        except Exception as e:
            print(f"TP error {path}: {e}")
            return None
    
    def map_sport(s):
        s = (s or "").lower()
        if "run" in s: return "run"
        if "bike" in s or "cycl" in s or "mtb" in s: return "bike"
        if "swim" in s: return "swim"
        if "strength" in s or "weight" in s: return "strength"
        return "other"
    
    # Buscar athlete ID
    user = tp_get("/users/v3/user")
    athlete_id = None
    if user:
        athlete_id = user.get("user", {}).get("userId") or user.get("userId")
    
    if not athlete_id:
        print("TP: nao conseguiu obter athlete ID")
        return
    
    print(f"TP athlete ID: {athlete_id}")
    
    # Buscar treinos planejados
    workouts = tp_get(f"/fitness/v6/athletes/{athlete_id}/workouts/{start}/{end}")
    
    if not workouts:
        print("TP: sem treinos encontrados")
        return
    
    if isinstance(workouts, dict):
        workouts = workouts.get("workouts", workouts.get("items", []))
    
    # Mapeamento correto de workoutTypeValueId -> sport (verificado nos dados reais)
    TYPE_ID_MAP = {
        1: "swim",      # Natacao
        2: "bike",      # Ciclismo
        3: "run",       # Corrida
        4: "run",       # Corrida trail
        5: "other",     # Outro
        6: "other",     # Outro
        7: "other",     # Day Off
        8: "bike",      # MTB / Indoor bike
        9: "strength",  # Forca
        10: "other",
        11: "swim",
        12: "run",
        13: "other",
        14: "bike",
        20: "strength",
    }

    saved = 0
    for w in workouts:
        date = (w.get("workoutDay") or w.get("WorkoutDay") or "")[:10]
        if not date: continue
        
        title = w.get("title") or w.get("Title") or ""
        
        # Usar typeId ou nome do tipo
        type_id = w.get("workoutTypeValueId") or 0
        type_name = w.get("workoutType") or w.get("WorkoutType") or ""
        sport = TYPE_ID_MAP.get(type_id) or map_sport(type_name) or map_sport(title)
        if sport == "other": continue
        
        dur_s = w.get("totalTimePlanned") or 0
        dur_min = round(dur_s / 60) if dur_s else None
        if not dur_min:
            dur_h = w.get("PlannedDuration") or w.get("plannedDuration") or 0
            dur_min = round(float(dur_h) * 60) if dur_h else None
        
        coach_notes = w.get("coachComments") or w.get("CoachComments") or w.get("description") or ""
        tss = w.get("tssPlanned") or w.get("TotalWork") or None
        
        planned = {
            "user_id": USER_ID,
            "date": date,
            "sport": sport,
            "title": title,
            "source": "trainingpeaks",
        }
        if dur_min: planned["duration_min"] = dur_min
        if coach_notes: planned["coach_notes"] = str(coach_notes)[:500]
        if tss: planned["tss_planned"] = float(tss)
        
        # Deletar e reinserir
        del_url = f"{SUPABASE_URL}/rest/v1/planned_workouts?user_id=eq.{USER_ID}&date=eq.{date}&sport=eq.{sport}"
        del_req = urllib.request.Request(del_url, method="DELETE")
        del_req.add_header("apikey", SUPABASE_KEY)
        del_req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
        try: urllib.request.urlopen(del_req)
        except: pass
        
        ins_url = f"{SUPABASE_URL}/rest/v1/planned_workouts"
        body = json.dumps(planned).encode()
        ins_req = urllib.request.Request(ins_url, data=body, method="POST")
        ins_req.add_header("apikey", SUPABASE_KEY)
        ins_req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
        ins_req.add_header("Content-Type", "application/json")
        ins_req.add_header("Prefer", "return=minimal")
        try:
            urllib.request.urlopen(ins_req)
            print(f"TP salvo: {sport} {date} {title[:30]}")
            saved += 1
        except Exception as e:
            print(f"TP erro salvar: {e}")
    
    print(f"TrainingPeaks: {saved} treinos sincronizados")


def sync_activities(api, today):
    import datetime
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    
    # Tipos a ignorar (Zwift duplica o indoor_cycling como virtual_ride)
    SKIP_TYPES = {"virtual_ride", "e_bike_fitness", "other"}
    
    # Mapeamento de tipos Garmin -> esportes do app
    SPORT_MAP = {
        "running": "run",
        "trail_running": "run",
        "treadmill_running": "run",
        "cycling": "bike",
        "indoor_cycling": "bike",
        "mountain_biking": "bike",
        "swimming": "swim",
        "open_water_swimming": "swim",
        "strength_training": "strength",
        "fitness_equipment": "strength",
    }
    
    try:
        activities = api.get_activities_by_date(yesterday, today)
        if not activities:
            print("Nenhuma atividade encontrada")
            return
        
        saved = 0
        for act in activities:
            act_type = act.get("activityType", {}).get("typeKey", "other")
            
            # Pular Zwift e tipos duplicados
            if act_type in SKIP_TYPES:
                print(f"Ignorando duplicata: {act.get('activityName')} ({act_type})")
                continue
            
            sport = SPORT_MAP.get(act_type)
            if not sport:
                print(f"Tipo desconhecido ignorado: {act_type}")
                continue
            
            dur_s = int(act.get("duration", 0))
            dist_m = int(act.get("distance", 0))
            avg_hr = act.get("averageHR")
            max_hr = act.get("maxHR")
            avg_power = act.get("avgPower")
            avg_speed = act.get("averageSpeed")
            avg_speed_kmh = round(avg_speed * 3.6, 1) if avg_speed else None
            start_time = act.get("startTimeLocal", "")
            date = start_time[:10] if start_time else yesterday
            title = act.get("activityName", sport.upper())
            
            workout = {
                "user_id": USER_ID,
                "date": date,
                "sport": sport,
                "title": title,
                "status": "completed",
                "actual_duration_s": dur_s,
                "actual_distance_m": dist_m,
            }
            if avg_hr: workout["avg_hr"] = int(avg_hr)
            if max_hr: workout["max_hr"] = int(max_hr)
            if avg_power: workout["avg_power_watts"] = int(avg_power)
            if avg_speed_kmh: workout["avg_speed_kmh"] = avg_speed_kmh
            
            # Verificar se já existe antes de inserir
            check_url = f"{SUPABASE_URL}/rest/v1/workouts?user_id=eq.{USER_ID}&date=eq.{date}&sport=eq.{sport}&select=id"
            import urllib.request
            req = urllib.request.Request(check_url)
            req.add_header("apikey", SUPABASE_KEY)
            req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
            try:
                import json
                resp = urllib.request.urlopen(req)
                existing = json.loads(resp.read())
                if existing:
                    print(f"Ja existe: {sport} {date} — pulando")
                    continue
            except: pass
            
            # Inserir novo treino
            ins_url = f"{SUPABASE_URL}/rest/v1/workouts"
            body = json.dumps(workout).encode()
            req2 = urllib.request.Request(ins_url, data=body, method="POST")
            req2.add_header("apikey", SUPABASE_KEY)
            req2.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
            req2.add_header("Content-Type", "application/json")
            req2.add_header("Prefer", "return=minimal")
            try:
                urllib.request.urlopen(req2)
                print(f"Treino salvo: {sport} {date} {dur_s//60}min FC:{int(avg_hr) if avg_hr else '?'}bpm")
                saved += 1
            except Exception as e:
                print(f"Erro ao salvar treino: {e}")
        
        print(f"{saved} treino(s) novo(s) sincronizado(s)")
    except Exception as e:
        print(f"Atividades erro: {e}")


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
    
    # Sincronizar treinos realizados
    sync_activities(api, today)
    
    # Sincronizar treinos planejados do TrainingPeaks
    sync_trainingpeaks()

if __name__ == "__main__":
    sync()
