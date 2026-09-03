import streamlit as st


def driver_card(profile):

    with st.container(border=True):

        left, right = st.columns([1, 2])

        # -----------------------------------------
        # Driver Portrait
        # -----------------------------------------

        with left:
            st.image(
                profile["image"],
                width=260,
            )

        # -----------------------------------------
        # Driver Information + Statistics
        # -----------------------------------------

        with right:

            st.title(profile["name"])

            st.write(f"🌍 **Nationality:** " f"{profile['nationality']}")

            st.write(f"🎂 **Age:** " f"{profile['age']}")

            st.write(f"🔢 **Driver Number:** " f"#{profile['number']}")

            st.divider()

            # -----------------------------------------
            # Driver Statistics
            # -----------------------------------------
            st.subheader("2026 Season Statistics")

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Championship Position",
                    profile["position"] if profile["position"] is not None else "-",
                )

            with c2:
                st.metric(
                    "Points",
                    profile["points"] if profile["points"] is not None else "-",
                )

            c3, c4 = st.columns(2)

            with c3:
                st.metric(
                    "Wins",
                    profile["wins"] if profile["wins"] is not None else "-",
                )

            with c4:
                st.metric(
                    "Team",
                    profile["team"] if profile["team"] is not None else "-",
                )




