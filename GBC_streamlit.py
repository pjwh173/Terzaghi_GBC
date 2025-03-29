import streamlit as st
import math

st.title("✨ Terzaghi's Ultimate Bearing Capacity Calculator ✨")

# Input values
c = st.number_input("Enter cohesion (c) in psf:", min_value=0.0, step=1.0)
phi = st.number_input("Enter angle of internal friction (ϕ) in degrees:", min_value=0.0, max_value=90.0, step=0.1)
q = st.number_input("Enter effective stress at foundation base (q) in psf:", min_value=0.0, step=1.0)
gamma = st.number_input("Enter unit weight of soil (γ) in pcf:", min_value=0.0, step=1.0)
Df = st.number_input("Enter depth of foundation (Df) in ft:", min_value=0.0, step=0.1)
B = st.number_input("Enter width of foundation (B) in ft:", min_value=0.0, step=0.1)
L = st.number_input("Enter length of foundation (L) in ft:", min_value=0.0, step=0.1)
beta = st.number_input("Enter load inclination angle (β) in degrees:", min_value=0.0, max_value=90.0, step=0.1)

if st.button("Calculate"):
    if min(c, phi, q, gamma, Df, B, L, beta) < 0:
        st.error("Error: values cannot be negative or zero.")
    else:
        phi_rad = math.radians(phi)

        # Terzaghi factors
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45) + phi_rad / 2))**2
        Nc = (Nq - 1) / math.tan(phi_rad) if phi != 0 else 5.7
        Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)

        # Shape factors
        Fcs = 1 + (B/L) * (Nq/Nc)
        Fqs = 1 + (B/L) * math.tan(phi_rad)
        Fgs = 1 - 0.4 * (B/L)

        # Depth factors
        if (Df/B <= 1):
            if phi == 0:
                Fcd = 1 + 0.4 * (Df/B)
                Fqd = 1
                Fgd = 1
            else:
                Fqd = 1 + 2 * math.tan(phi_rad) * (1 - math.sin(phi_rad))**2 * (Df/B)
                Fcd = Fqd - ((1 - Fqd) / (Nc * math.tan(phi_rad)))
                Fgd = 1
        else:
            if phi == 0:
                Fcd = 1 + (0.4 * math.atan(Df/B))
                Fqd = 1
                Fgd = 1
            else:
                Fqd = 1 + (2 * math.tan(phi_rad) * (1 - math.sin(phi_rad))**2 * math.atan(Df/B))
                Fcd = Fqd - ((1 - Fqd) / (Nc * math.tan(phi_rad)))
                Fgd = 1

        # Inclination factors
        Fci = Fqi = (1 - beta / 90)**2
        if phi == 0:
            Fgi = 1 
        else:
            Fgi = (1 - (beta / phi))**2

        # Display calculated factors
        st.subheader("Terzaghi Bearing Capacity Factors")
        st.write(f"Nc = {Nc:.3f}, Nq = {Nq:.3f}, Nγ = {Ngamma:.3f}")

        st.subheader("Shape Factors")
        st.write(f"Fcs = {Fcs:.3f}, Fqs = {Fqs:.3f}, Fγs = {Fgs:.3f}")

        st.subheader("Depth Factors")
        st.write(f"Fcd = {Fcd:.3f}, Fqd = {Fqd:.3f}, Fγd = {Fgd:.3f}")

        st.subheader("Inclination Factors")
        st.write(f"Fci = {Fci:.3f}, Fqi = {Fqi:.3f}, Fγi = {Fgi:.3f}")

        # Ultimate bearing capacity calculation (with factors)
        qu = (c * Nc * Fcs * Fcd * Fci) + (q * Nq * Fqs * Fqd * Fqi) + (0.5 * gamma * B * Ngamma * Fgs * Fgd * Fgi)

        st.subheader("🔥 Ultimate Bearing Capacity (qu) 🔥")
        st.success(f"{qu:.3f} lb/ft²")
