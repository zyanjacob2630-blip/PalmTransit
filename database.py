import sqlite3, json, datetime
from simulation import get_scenario
DB="palmtransit.sqlite"
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
    c=conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS routes(id TEXT PRIMARY KEY,name TEXT,stops TEXT);
    CREATE TABLE IF NOT EXISTS proposals(id TEXT PRIMARY KEY,route TEXT,reason TEXT,path TEXT,status TEXT,created TEXT);
    CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,time TEXT,action TEXT,details TEXT);
    """); c.commit(); c.close()
def log(action,details):
    c=conn(); c.execute("INSERT INTO audit(time,action,details) VALUES(?,?,?)",(datetime.datetime.now().isoformat(timespec="seconds"),action,details));c.commit();c.close()
def seed_db():
    c=conn()
    rows=[("R1","Route 1",["Library","Main Gate","Dorms","Sports Hall"]),("R2","Route 2",["Science Block","Main Gate","Student Center","Metro Link"]),("R3","Route 3",["Arts Block","Dorms","Clinic","Main Gate"])]
    for id,name,stops in rows:c.execute("INSERT OR IGNORE INTO routes VALUES(?,?,?)",(id,name,json.dumps(stops)))
    c.commit();c.close()
def get_routes():
    c=conn(); rows=c.execute("SELECT * FROM routes").fetchall();c.close()
    return [{"id":r["id"],"name":r["name"],"stops":json.loads(r["stops"])} for r in rows]
def get_route_status(route_id):
    scenario=get_scenario()
    status,source,msg,updated="On schedule","GPS","GPS feed is fresh; no disruption detected.","09:52"
    if scenario=="Sandstorm": status,source,msg="Safety alert","Weather alert","Sandstorm alert: service may be delayed. Safety notice takes priority over GPS and timetable."
    elif scenario=="Convocation roadblock": status,source,msg="Disrupted","Campus event","Convocation barrier affects the central road. Route adjustment is being considered."
    elif scenario=="GPS conflict": status,source,msg="Feed conflict","Resolver","GPS conflicts with timetable. Valid fresh GPS is used; timetable remains fallback."
    elif scenario=="Stale GPS": status,source,msg="Stale GPS","Timetable fallback","GPS is older than the freshness threshold. Timetable fallback is shown; live position is not asserted."
    elif scenario=="Dark GPS": status,source,msg="GPS unavailable","Timetable fallback","GPS feed is unavailable. Only timetable-based guidance is provided."
    elif scenario=="Crowd surge": status,source,msg="Crowding","Crowd feed","Crowd surge detected at a stop. Consider nearby alternatives."
    elif scenario=="Accessibility disruption": status,source,msg="Accessibility warning","Stop data","A stop accessibility issue is simulated. Recommend accessible alternatives."
    elif scenario=="Combined disruption": status,source,msg="Multiple alerts","Safety resolver","Sandstorm and event barrier simulated. Safe alternatives are prioritized; route changes require approval."
    return {"status":status,"source":source,"message":msg,"updated":updated}
def get_alerts():
    s=get_scenario()
    return [] if s=="Normal" else [f"Demo scenario active: {s}. Treat this as simulated operational data."]
def get_stop_recommendations(route,accessible=False):
    stops=[("Main Gate",92,"Shade, access ramp, low crowding"),("Student Center",86,"Sheltered and nearby"),("Library",78,"Accessible path, moderate crowding"),("Metro Link",74,"Covered waiting area")]
    if accessible: stops=sorted(stops,key=lambda x:("ramp" not in x[2],-x[1]))
    return [{"stop":s,"score":score,"reason":why} for s,score,why in stops]
def get_proposals(status=None):
    c=conn(); rows=c.execute("SELECT * FROM proposals "+("WHERE status=?" if status else "ORDER BY created DESC"),(status,) if status else ()).fetchall();c.close()
    return [{"id":r["id"],"route":r["route"],"reason":r["reason"],"path":json.loads(r["path"]),"status":r["status"]} for r in rows]
def stage(route,reason,path):
    import uuid
    pid="RP-"+uuid.uuid4().hex[:6].upper()
    c=conn();c.execute("INSERT INTO proposals VALUES(?,?,?,?,?,?)",(pid,route,reason,json.dumps(path),"pending",datetime.datetime.now().isoformat(timespec="seconds")));c.commit();c.close()
    log("Reroute staged",f"{pid} {route}: {reason}");return pid
def approve_proposal(pid,officer):
    c=conn();c.execute("UPDATE proposals SET status='approved' WHERE id=? AND status='pending'",(pid,));c.commit();c.close();log("Reroute approved",f"{pid} by {officer}")
def reject_proposal(pid,officer,reason):
    c=conn();c.execute("UPDATE proposals SET status='rejected' WHERE id=? AND status='pending'",(pid,));c.commit();c.close();log("Reroute rejected",f"{pid} by {officer}: {reason}")
def get_audit():
    c=conn();rows=c.execute("SELECT * FROM audit ORDER BY id DESC LIMIT 100").fetchall();c.close();return [dict(r) for r in rows]
