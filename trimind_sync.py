import sys, os
sys.path.insert(0, '/Users/josevictorfrancisco/Library/Python/3.9/lib/python/site-packages')
from garminconnect import Garmin
import datetime, urllib.request, json

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://rotzznmlcrqwtrxesezn.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvdHp6bm1sY3Jxd3RyeGVzZXpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkzODEwMTgsImV4cCI6MjA5NDk1NzAxOH0.rbGvnLTvWRmA-217TBplQXPTWHeZHUmkaeMk_BSfLp0")
USER_ID = "4385160f-c76f-4649-973f-fb0f8f92065b"
GARMIN_EMAIL = os.environ.get("GARMIN_EMAIL", "jvictorvf@hotmail.com")
GARMIN_PASSWORD = os.environ.get("GARMIN_PASSWORD", "Iglu45220052.")

RACE_DATE = datetime.date(2026, 9, 20)

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

def supabase_query(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}"
    req = urllib.request.Request(url)
    req.add_header("apikey", SUPABASE_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
    req.add_header("Accept", "application/json")
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except Exception as e:
        print(f"Supabase query error: {e}")
        return []

def sync_trainingpeaks():
    TP_COOKIE = os.environ.get("TP_COOKIE", "Production_tpAuth=V001aheYPkwmKUmw75FR4_utn_e8GPafFLnjYbL212ZOIGtAToHIO0BarKJ9NdVazjlDi8TVSEscv1o-Pq7tNReQZsost2oCu_vB21QgDf6EB4Dph2LB3qKgk6po9yR8w4J8wU0ZP6-4qxgUGfHNRr171SIcBcxQ3pvwaiv4fHvCK6rbXnSuH3fJ6atZvEha_KojBcGBfCSI5q-uxWEZUoSrYnhN6_gVTcjVHcC21AIQccfVEx3YWzQiy8zYI2Anf5zAyeCWnx_TQ_uKzf0g7VBBy7J83p12Ks2lUeEpVPLjQVZuSytAp4056HH2_8ZVDP-2KN3CaxS-eCi1EqyWsOcYG1WH2pQ-fB2dC7x8ZVeY3t1h4eeSLzrl8xAqdKEP9q1OTXx3j0lcFSJl-E-oBOMQGNiAmVcMikejnwQjBYMd9JH5xcH4gdvek4kXkeL7esaUsoxGGa8tO9ZEiIA0q_B0nsKXxMaCpvvxugotaJggNpl0gtVdDegmml9wcFrw1eKMEMLxP6hm4ooq8gpT-BHfzkX2ACh3kCHstWPk-zTXp0g1-aGIEKKIhr4Sur4dTNAIQMPw69uxPC6ChLMiw9RX5GldWoqHFZqeIulaL7ZmUmC9gBgIHfMVJevBqFYc1u1eWUetP5egNlYuYHVqRFGdA3yv5PKBAlUtvMsK3dQIezVHXQPx_chFyrYG5G2DV4WOeU0JmMuM1YOchlv5nfzukFQHJeilELy06nWDFs_JxjpREjUGYrVj539Rrzc4ifYryX34c6pqRFabCm3SXI2f6lhanpkl8N-16z8kfSv7aIJFCXTCu0B6TxMrS8spCKR4NrPvG5m9byBOfcfir_5C_u6jOaT0A3VAXk7kz4gAhpLcs89Ce8yf-vrW5v1kl7KQalqSs_-4z8xCnZ8xDIzTiDEp-F4Rd6zBOHSzh0bcQyzAnLAXeLFkWLaYXFlIm0AkNVZe3fvBCTKADHWMcpMPEEDRXSxaq4v2ZOYF0Gb_bq9Vg7EmLqvgPNG23V3aP_CBD7Yv5eFToufrhS7_JEtPZEkq2nKzI4aPXfdhqlJ8a-63Rdc846uR3ecuvx4ATTMt6JKrmwXyDXSoBlc0atVWy4PQQd6TbpvuPNHQF3p40Y8HZ_88G-nl5ZqYqVFY2d6Ano-E7obBuN6uTBDz7_2a1pkY8-XicuppmD9pjZNJfjOJBQsR3Xm1GDCYLady5w8N4B_cPp2oSacgcF4_kW4b57auc8UeH-xoki9wpFpFoGG7yXhlgYx0d3WUe1txRgySP7W2lOAOzoCAQh4KwitwJ2L3iNEl0ocWcZ1KewOeR7izQ22IljiCWk8huiTmVsCz0aEOHU56DA-hLb_QvHM2nuqNFKrW4ResEdf2mJ-kHddSyyCmpTUnLHj7JyHsMHm3PCIgPFI-ioVBurqCrQw5SNeBSKxuTarkTrkmlGdVszp04MLekXQG5hFuy8kXB8OzBbtF7534U_hBH5Hd75HVa8m1P6b2DAmNBNCd6Z3BWLml8yvBAWQIaWa5uOyu2PmW9qdfBwxTJhIC-mhGqKNPjo2TifjVmfOYO4kdEUHbdzqyOssg46Xg44Ck0PBrVr3VHsYH4hPI2m2h0-2mdUjMYKkaPXGGeHIClwQ1z22V0Fzu4_1eRtaPqAFtfUW3uX-LoIpaNNLnwrUjB63i9FQ83hFD8YjeaFVy_8ts11uyQYGD0sMwjwHx_suNa9rny-Gdse4Hrd5Ovt-wojAVy_sQR-uVMHDnaXmdRSlDb_TOoTs1")

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
        if "run" in s or "corrida" in s: return "run"
        if "bike" in s or "cycl" in s or "mtb" in s: return "bike"
        if "swim" in s or "natacao" in s or "natação" in s: return "swim"
        if "strength" in s or "forca" in s or "força" in s or "weight" in s: return "strength"
        return "other"

    TYPE_ID_MAP = {
        1: "swim", 2: "bike", 3: "run", 4: "run", 5: "other",
        6: "other", 7: "other", 8: "bike", 9: "strength",
        10: "other", 11: "swim", 12: "run", 13: "other",
        14: "bike", 20: "strength",
    }

    def detect_workout_category(title):
        t = (title or "").upper()
        if any(x in t for x in ["VO2", "VMAX"]): return "vo2max"
        if any(x in t for x in ["LIMIAR", "THRESHOLD", "Z4", "LT"]): return "limiar"
        if any(x in t for x in ["CONT", "CONTINUO", "CONTÍNUO", "AEROB"]): return "aerobico"
        if any(x in t for x in ["FORCA", "FORÇA", "STRENGTH", "GYM", "APP"]): return "forca"
        if any(x in t for x in ["REG", "REGENERATIVO", "RECOVERY"]): return "recuperacao"
        if any(x in t for x in ["LONG", "LONGO", "ENDURANCE"]): return "longo"
        if any(x in t for x in ["T1", "T2", "TEMPO", "RACE"]): return "tempo"
        if any(x in t for x in ["AULA", "CLASS"]): return "aula"
        return "geral"

    user = tp_get("/users/v3/user")
    athlete_id = None
    if user:
        athlete_id = user.get("user", {}).get("userId") or user.get("userId")
    if not athlete_id:
        print("TP: nao conseguiu obter athlete ID")
        return
    print(f"TP athlete ID: {athlete_id}")

    # CTL / ATL / TSB
    ctl = atl = tsb = None
    load_data = tp_get(f"/fitness/v1/athletes/{athlete_id}/fitness")
    if not load_data:
        load_data = tp_get(f"/fitness/v6/athletes/{athlete_id}/fitness/{start}/{start}")
    if load_data:
        entry = load_data[-1] if isinstance(load_data, list) and load_data else load_data if isinstance(load_data, dict) else {}
        ctl = entry.get("ctl") or entry.get("CTL") or entry.get("fitnessScore")
        atl = entry.get("atl") or entry.get("ATL") or entry.get("fatigueScore")
        tsb = entry.get("tsb") or entry.get("TSB") or entry.get("formScore")
        if ctl or atl or tsb:
            print(f"Carga: CTL={ctl} ATL={atl} TSB={tsb}")
        else:
            print(f"TP: CTL/ATL/TSB nao encontrado (campos disponiveis: {list(entry.keys())[:8]})")
    else:
        print("TP: endpoint fitness nao disponivel")

    # Semanas ate a prova
    weeks_to_race = round((RACE_DATE - today).days / 7, 1)
    print(f"Semanas ate IRONMAN 70.3 SP: {weeks_to_race}")

    # Compliance 4 semanas
    four_weeks_ago = (today - datetime.timedelta(days=28)).isoformat()
    completed_workouts = supabase_query("workouts", f"user_id=eq.{USER_ID}&date=gte.{four_weeks_ago}&date=lt.{start}&status=eq.completed&select=id")
    planned_past = supabase_query("planned_workouts", f"user_id=eq.{USER_ID}&date=gte.{four_weeks_ago}&date=lt.{start}&select=id")
    compliance_pct = round(len(completed_workouts) / len(planned_past) * 100) if planned_past else None
    print(f"Compliance 4 semanas: {len(completed_workouts)}/{len(planned_past)} = {compliance_pct}%")

    # Treinos planejados
    workouts = tp_get(f"/fitness/v6/athletes/{athlete_id}/workouts/{start}/{end}")
    if not workouts:
        print("TP: sem treinos encontrados")
        return
    if isinstance(workouts, dict):
        workouts = workouts.get("workouts", workouts.get("items", []))

    # Fase do plano
    def detect_plan_phase(wlist):
        titles = " ".join([w.get("title","") for w in wlist]).upper()
        if any(x in titles for x in ["TAPER", "AFUNILAMENTO", "RACE WEEK"]): return "taper"
        if weeks_to_race <= 2: return "taper"
        if any(x in titles for x in ["VO2", "VMAX", "INTENSIDADE"]): return "build"
        if weeks_to_race <= 10: return "build"
        return "base"

    plan_phase = detect_plan_phase(workouts)
    print(f"Fase do plano: {plan_phase}")

    next_7_end = (today + datetime.timedelta(days=7)).isoformat()
    weekly_tss_planned = sum(
        float(w.get("tssPlanned") or 0)
        for w in workouts
        if start <= (w.get("workoutDay","")[:10]) < next_7_end
    )
    print(f"TSS planejado proximos 7 dias: {round(weekly_tss_planned)}")

    # Salvar contexto em daily_metrics
    plan_context = {"user_id": USER_ID, "date": start, "weeks_to_race": weeks_to_race, "plan_phase": plan_phase}
    if weekly_tss_planned: plan_context["weekly_tss_planned"] = round(weekly_tss_planned)
    if compliance_pct is not None: plan_context["compliance_4w_pct"] = compliance_pct
    if ctl is not None: plan_context["ctl"] = float(ctl)
    if atl is not None: plan_context["atl"] = float(atl)
    if tsb is not None: plan_context["tsb"] = float(tsb)
    supabase_upsert("daily_metrics", plan_context)
    print(f"Contexto do plano salvo!")

    # Salvar treinos planejados
    saved = 0
    for w in workouts:
        date = (w.get("workoutDay") or "")[:10]
        if not date: continue
        title = w.get("title") or ""
        type_id = w.get("workoutTypeValueId") or 0
        sport = TYPE_ID_MAP.get(type_id) or map_sport(w.get("workoutType","")) or map_sport(title)
        if sport == "other": continue

        dur_s = w.get("totalTimePlanned") or 0
        dur_min = round(dur_s / 60) if dur_s else None
        if not dur_min:
            dur_h = w.get("plannedDuration") or 0
            dur_min = round(float(dur_h) * 60) if dur_h else None

        coach_notes = w.get("coachComments") or w.get("description") or ""
        tss = w.get("tssPlanned") or None
        dist_m = w.get("distancePlanned") or None
        if_planned = w.get("ifPlanned") or None
        workout_category = detect_workout_category(title)

        planned = {
            "user_id": USER_ID, "date": date, "sport": sport,
            "title": title, "source": "trainingpeaks",
            "workout_category": workout_category,
        }
        if dur_min: planned["duration_min"] = dur_min
        if coach_notes: planned["coach_notes"] = str(coach_notes)[:500]
        if tss: planned["tss_planned"] = float(tss)
        if dist_m: planned["distance_planned_m"] = round(float(dist_m))
        if if_planned: planned["if_planned"] = float(if_planned)

        del_url = f"{SUPABASE_URL}/rest/v1/planned_workouts?user_id=eq.{USER_ID}&date=eq.{date}&sport=eq.{sport}"
        del_req = urllib.request.Request(del_url, method="DELETE")
        del_req.add_header("apikey", SUPABASE_KEY)
        del_req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
        try: urllib.request.urlopen(del_req)
        except: pass

        ins_req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/planned_workouts", data=json.dumps(planned).encode(), method="POST")
        ins_req.add_header("apikey", SUPABASE_KEY)
        ins_req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
        ins_req.add_header("Content-Type", "application/json")
        ins_req.add_header("Prefer", "return=minimal")
        try:
            urllib.request.urlopen(ins_req)
            print(f"TP salvo: {sport} {date} [{workout_category}] {title[:30]}")
            saved += 1
        except Exception as e:
            print(f"TP erro salvar: {e}")

    print(f"TrainingPeaks: {saved} treinos sincronizados")


def sync_activities(api, today):
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    SKIP_TYPES = {"virtual_ride", "e_bike_fitness", "other"}
    SPORT_MAP = {
        "running": "run", "trail_running": "run", "treadmill_running": "run",
        "cycling": "bike", "indoor_cycling": "bike", "mountain_biking": "bike",
        "swimming": "swim", "open_water_swimming": "swim",
        "strength_training": "strength", "fitness_equipment": "strength",
    }
    try:
        activities = api.get_activities_by_date(yesterday, today)
        if not activities:
            print("Nenhuma atividade encontrada")
            return
        saved = 0
        for act in activities:
            act_type = act.get("activityType", {}).get("typeKey", "other")
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
            tss_garmin = act.get("trainingStressScore") or act.get("tss") or None

            workout = {
                "user_id": USER_ID, "date": date, "sport": sport,
                "title": title, "status": "completed",
                "actual_duration_s": dur_s, "actual_distance_m": dist_m,
            }
            if avg_hr: workout["avg_hr"] = int(avg_hr)
            if max_hr: workout["max_hr"] = int(max_hr)
            if avg_power: workout["avg_power_watts"] = int(avg_power)
            if avg_speed_kmh: workout["avg_speed_kmh"] = avg_speed_kmh
            if tss_garmin: workout["tss_actual"] = float(tss_garmin)

            check_req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/workouts?user_id=eq.{USER_ID}&date=eq.{date}&sport=eq.{sport}&select=id")
            check_req.add_header("apikey", SUPABASE_KEY)
            check_req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
            try:
                existing = json.loads(urllib.request.urlopen(check_req).read())
                if existing:
                    print(f"Ja existe: {sport} {date} — pulando")
                    continue
            except: pass

            ins_req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/workouts", data=json.dumps(workout).encode(), method="POST")
            ins_req.add_header("apikey", SUPABASE_KEY)
            ins_req.add_header("Authorization", f"Bearer {SUPABASE_KEY}")
            ins_req.add_header("Content-Type", "application/json")
            ins_req.add_header("Prefer", "return=minimal")
            try:
                urllib.request.urlopen(ins_req)
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
    sync_activities(api, today)
    sync_trainingpeaks()

if __name__ == "__main__":
    sync()
