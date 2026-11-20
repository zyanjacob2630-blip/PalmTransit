import streamlit as st
from database import init_db, seed_db, get_routes, get_route_status, get_alerts, get_stop_recommendations, get_proposals, approve_proposal, reject_proposal, get_audit
from agent import answer_commuter, create_reroute_proposal
from simulation import set_scenario, get_scenario

st.set_page_config(page_title="PalmTransit", page_icon="🚌", layout="wide")
init_db(); seed_db()
st.title("🚌 PalmTransit")
st.caption("Campus shuttle disruption & commuter assistant · Demo prototype")

with st.sidebar:
    st.header("Simulation")
    scenario = st.selectbox("Scenario", ["Normal", "Sandstorm", "Convocation roadblock", "GPS conflict", "Stale GPS", "Dark GPS", "Crowd surge", "Accessibility disruption", "Combined disruption"])
    if scenario != get_scenario(): set_scenario(scenario)
    st.info("Demo data is simulated. Reroute proposals require officer approval.")
    page=st.radio("Navigate", ["Overview","Live Shuttle Status","Commuter AI","Smart Stop Finder","Reroute Management","Officer Console","Audit Log"])

routes=get_routes()
if page=="Overview":
    cols=st.columns(4)
    cols[0].metric("Routes",len(routes)); cols[1].metric("Campus riders","~3,000")
    cols[2].metric("Scenario",get_scenario()); cols[3].metric("Pending proposals",len(get_proposals("pending")))
    st.subheader("Route overview")
    for r in routes:
        status=get_route_status(r["id"])
        with st.container(border=True):
            st.markdown(f"**{r['name']}** · {status['status']} · {status['source']}")
            st.write(status["message"])
    st.subheader("Active alerts")
    for a in get_alerts(): st.warning(a)

elif page=="Live Shuttle Status":
    for r in routes:
        s=get_route_status(r["id"])
        st.subheader(r["name"])
        st.write(f"**Status:** {s['status']}  | **Feed:** {s['source']}  | **Last update:** {s['updated']}")
        st.write(s["message"])
        st.caption(f"Stops: {', '.join(r['stops'])}")

elif page=="Commuter AI":
    st.subheader("Ask about shuttle service")
    q=st.text_input("Question",placeholder="Is Route 2 running? Where should I board?")
    route=st.selectbox("Optional route",["All routes"]+[r["name"] for r in routes])
    if st.button("Ask PalmTransit",type="primary") and q:
        with st.spinner("Checking the service feeds..."):
            st.markdown(answer_commuter(q,None if route=="All routes" else route))
    st.caption("Answers are grounded in demo feeds and rule-based status resolution.")

elif page=="Smart Stop Finder":
    st.subheader("Recommended boarding stops")
    route=st.selectbox("Route", [r["name"] for r in routes])
    needs_access=st.checkbox("Prioritize accessible stops")
    for item in get_stop_recommendations(route,needs_access):
        st.write(f"**{item['stop']}** — score {item['score']}/100")
        st.caption(item["reason"])

elif page=="Reroute Management":
    st.subheader("Stage a reroute")
    route=st.selectbox("Route to reroute", [r["name"] for r in routes])
    reason=st.text_area("Reason", "Avoid affected roads during the current disruption.")
    if st.button("Generate proposal"):
        p=create_reroute_proposal(route,reason)
        st.success(f"Proposal {p} staged. It is not live until approved.")
    st.write("Proposals")
    for p in get_proposals():
        st.write(f"**{p['id']}** · {p['route']} · {p['status']}")
        st.caption(p["reason"])

elif page=="Officer Console":
    st.subheader("Transport Officer approval")
    pending=get_proposals("pending")
    if not pending: st.info("No pending proposals.")
    for p in pending:
        with st.container(border=True):
            st.write(f"**{p['id']} — {p['route']}**")
            st.write(p["reason"]); st.write("Proposed path: "+ " → ".join(p["path"]))
            c1,c2=st.columns(2)
            if c1.button("Approve",key="approve"+p["id"]):
                approve_proposal(p["id"],"demo_officer"); st.success("Approved and recorded."); st.rerun()
            if c2.button("Reject",key="reject"+p["id"]):
                reject_proposal(p["id"],"demo_officer","Rejected in demo console"); st.warning("Rejected and recorded."); st.rerun()

elif page=="Audit Log":
    st.subheader("Decision audit trail")
    for e in get_audit():
        st.write(f"`{e['time']}` · **{e['action']}** · {e['details']}")
