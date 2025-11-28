import time

def complex_calculation():
    print("Starting complex calculation...")
    total = 0
    # Simulate work with loops
    for i in range(100):
        for j in range(100):
            total += i * j
            
    # Simulate conditional
    if total > 1000:
        print(f"Total is large: {total}")
    else:
        print("Total is small")
        
    time.sleep(2)
    print("Calculation complete!")

if __name__ == "__main__":
    complex_calculation()
