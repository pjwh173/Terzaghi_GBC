import math

def terzaghi_bearing_capacity():
    print("✨ Terzaghi's Ultimate Bearing Capacity Calculator✨\n")

    # Input values
    c = float(input("Enter cohesion (c) in psf: "))
    phi = float(input("Enter angle of internal friction (ϕ) in degrees: "))
    q = float(input("Enter effective stress at foundation base (q) in psf: "))
    gamma = float(input("Enter unit weight of soil (γ) in pcf: "))
    Df = float(input("Enter depth of foundation (Df) in ft: "))
    B = float(input("Enter width of foundation (B) in ft: "))
    L = float(input("Enter length of foundation (L) in ft: "))
    beta = float(input("Enter load inclination angle (β) in degrees: "))

    # Error for entered negative values
    if min(c, phi, gamma, Df, B, L, beta) < 0:
        print("Error: values cannot be negative or zero. Are you stupid?")
        return

    phi_rad = math.radians(phi)
    beta_rad = math.radians(beta)

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
        pass
    Fgi = (1 -  ( beta / phi ) )**2

    # Display calculated factors
    print("\n--- Terzaghi Bearing Capacity Factors ---")
    print(f"Nc = {Nc:.3f}, Nq = {Nq:.3f}, Nγ = {Ngamma:.3f}")

    print("\n--- Shape Factors ---")
    print(f"Fcs = {Fcs:.3f}, Fqs = {Fqs:.3f}, Fγs = {Fgs:.3f}")

    print("\n--- Depth Factors ---")
    print(f"Fcd = {Fcd:.3f}, Fqd = {Fqd:.3f}, Fγd = {Fgd:.3f}")

    print("\n--- Inclination Factors ---")
    print(f"Fci = {Fci:.3f}, Fqi = {Fqi:.3f}, Fγi = {Fgi:.3f}")

    # Ultimate bearing capacity calculation (with factors)
    qu = (c * Nc * Fcs * Fcd * Fci) + (q * Nq * Fqs * Fqd * Fqi) + (0.5 * gamma * B * Ngamma * Fgs * Fgd * Fgi)

    # Display result
    print("\n🔥 Ultimate Bearing Capacity (qu) 🔥")
    print(f"qu = {qu:.3f} lb/ft²")

# Run the calculator
if __name__ == "__main__":
    terzaghi_bearing_capacity()
