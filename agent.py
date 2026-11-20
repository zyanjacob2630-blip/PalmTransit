from database import get_routes,get_route_status,get_stop_recommendations,stage,log
from simulation import get_scenario
def answer_commuter(question,route_name=None):
    routes=get_routes(); selected=[r for r in routes if route_name is None or r["name"]==route_name]
    status_lines=[]
    for r in selected:
        s=get_route_status(r["id"]); status_lines.append(f"{r['name']}: {s['status']}. {s['message']}")
    # Rule-grounded response; the LLM is intentionally optional in this starter build.
    msg="I checked the simulated service feeds.\\n\\n"+"\\n\\n".join(status_lines)
    if any(k in question.lower() for k in ["stop","board","where"]):
        msg+="\\n\\nSuggested boarding stops: "+", ".join(x["stop"] for x in get_stop_recommendations(selected[0]["name"] if selected else "Route 1")[:3])+"."
    msg+="\\n\\nI cannot confirm a real-time arrival from this demo dataset."
    log("Commuter query",question[:180])
    return msg
def create_reroute_proposal(route_name,reason):
    route=next(r for r in get_routes() if r["name"]==route_name)
    path=route["stops"][:]
    if get_scenario()!="Normal": path.insert(1,"Alternative safe corridor (simulated)")
    return stage(route_name,reason,path)
