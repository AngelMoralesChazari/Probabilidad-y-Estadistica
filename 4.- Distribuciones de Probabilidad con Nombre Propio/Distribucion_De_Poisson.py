import math

def poisson_approximation_binomial():
    print("\n=== APROXIMACIÓN POISSON DE BINOMIAL ===")
    try:
        n = int(input("Ingrese n (número de ensayos): "))
        p = float(input("Ingrese p (probabilidad de éxito): "))
        k = int(input("Ingrese k (número de éxitos deseados): "))
    except ValueError:
        print("❌ Error: Ingrese números enteros para n y k, y un número para p.")
        return
    
    lambda_val = n * p
    
    # Verificar condiciones
    print(f"\nParámetros: n = {n}, p = {p}, λ = {lambda_val:.4f}")
    
    condiciones = True
    if n < 30:
        print("⚠️  n < 30 - podría no ser ideal para aproximación Poisson")
        condiciones = False
    if p > 0.1:
        print("⚠️  p > 0.1 - podría no ser ideal para aproximación Poisson")
        condiciones = False
    if lambda_val > 20:
        print("⚠️  λ > 20 - podría ser mejor usar aproximación normal")
    
    if condiciones and lambda_val <= 20:
        print("✅ Condiciones adecuadas para aproximación Poisson")
    
    # Cálculo Poisson: P(X=k)
    try:
        prob_poisson = math.exp(-lambda_val) * (lambda_val ** k) / math.factorial(k)
    except:
        print("❌ Error: El cálculo de Poisson falló (posiblemente k! o λ^k demasiado grande).")
        return
    
    print(f"\nRESULTADOS:")
    print(f"Probabilidad Poisson P(X = {k}) = {prob_poisson:.6f}")
    
    # Opcional: cálculo binomial exacto para comparar
    try:
        prob_binomial = math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
        print(f"Probabilidad Binomial exacta = {prob_binomial:.6f}")
        print(f"Diferencia = {abs(prob_poisson - prob_binomial):.6f}")
    except:
        print("No se pudo calcular binomial exacta (n muy grande)")

def poisson_direct():
    print("\n=== DISTRIBUCIÓN POISSON DIRECTA ===")
    try:
        lambda_val = float(input("Ingrese λ (lambda/tasa promedio): "))
    except ValueError:
        print("❌ Error: Ingrese un número para lambda.")
        return
        
    tipo = input("¿Qué probabilidad quiere? P(X=k) [=], P(X<=k) [<=] o P(X>=k) [>=]: ")
    
    if tipo == "=":
        try:
            k = int(input("Ingrese k: "))
            prob = math.exp(-lambda_val) * (lambda_val ** k) / math.factorial(k)
            print(f"\nRESULTADO: P(X = {k}) = {prob:.6f}")
        except:
            print("❌ Error en el cálculo o entrada no válida para k.")
            
    elif tipo == "<=":
        try:
            k = int(input("Ingrese k máximo: "))
            prob_acumulada = 0
            
            print("\nDesglose de Probabilidades Individuales:")
            for i in range(k + 1):
                p_i = math.exp(-lambda_val) * (lambda_val ** i) / math.factorial(i)
                prob_acumulada += p_i
                print(f"P(X = {i}) = {p_i:.6f}")
                
            print(f"\nRESULTADO: P(X ≤ {k}) = {prob_acumulada:.6f}")

        except:
            print("❌ Error en el cálculo o entrada no válida para k.")

    elif tipo == ">=":
        try:
            k = int(input("Ingrese k mínimo (cuando menos): "))
            
            # Cálculo de la probabilidad de al menos k mediante el complemento: P(X >= k) = 1 - P(X <= k-1)
            k_complemento = k - 1
            
            if k_complemento < 0:
                # P(X >= 0) siempre es 1 en distribuciones discretas
                prob_final = 1.0
                print(f"\nRESULTADO: P(X ≥ {k}) = {prob_final:.6f} (P(X >= 0) es 1)")
                return

            prob_acumulada_complemento = 0
            
            print(f"\nCálculo de Complemento: P(X ≥ {k}) = 1 - P(X ≤ {k_complemento})")
            print("Desglose de P(X ≤ {k_complemento}):")
            
            for i in range(k_complemento + 1):
                p_i = math.exp(-lambda_val) * (lambda_val ** i) / math.factorial(i)
                prob_acumulada_complemento += p_i
                print(f"P(X = {i}) = {p_i:.6f}")
            
            prob_final = 1.0 - prob_acumulada_complemento
            
            print(f"\nP(X ≤ {k_complemento}) = {prob_acumulada_complemento:.6f}")
            print(f"RESULTADO: P(X ≥ {k}) = 1 - {prob_acumulada_complemento:.6f} = {prob_final:.6f}")

        except:
            print("❌ Error en el cálculo o entrada no válida para k.")

    else:
        print("Opción de cálculo no válida. Use '=', '<=' o '>='.")

def main():
    print("CALCULADORA DE PROBABILIDAD - POISSON")
    print("=" * 50)
    
    while True:
        print("\nSeleccione el tipo de problema:")
        print("1. Aproximación Poisson de Binomial")
        print("2. Distribución Poisson directa")
        print("3. Salir")
        
        opcion = input("\nIngrese su opción (1-3): ")
        
        if opcion == "1":
            poisson_approximation_binomial()
        elif opcion == "2":
            poisson_direct()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()