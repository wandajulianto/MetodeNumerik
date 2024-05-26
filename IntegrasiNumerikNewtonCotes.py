import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, lambdify, symbols
import sympy as sp

class IntegrasiNumerik:
    def __init__(self, fungsi_str, a, b, n, variabel, nilai_var):
        self.fungsi_str = fungsi_str
        self.a = a
        self.b = b
        self.n = n
        self.variabel = variabel
        self.nilai_var = nilai_var
        self.x = symbols('x')
        self.fungsi_expr = sympify(self.fungsi_str)
        self.f = lambdify((self.x, *self.variabel), self.fungsi_expr, 'numpy')

    def kaidah_trapesium(self):
        h = (self.b - self.a) / self.n
        jumlah = self.f(self.a, *self.nilai_var) + self.f(self.b, *self.nilai_var)
        for i in range(1, self.n):
            xi = self.a + i * h
            jumlah += 2 * self.f(xi, *self.nilai_var)
        integral = (h / 2) * jumlah
        return integral, h

    def kaidah_simpson_1_3(self):
        if self.n % 2 != 0:
            raise ValueError("Nilai n harus genap.")
        h = (self.b - self.a) / self.n
        jumlah_ganjil = 0
        jumlah_genap = 0
        for i in range(1, self.n):
            xi = self.a + i * h
            if i % 2 == 0:
                jumlah_genap += self.f(xi, *self.nilai_var)
            else:
                jumlah_ganjil += self.f(xi, *self.nilai_var)
        integral = (h / 3) * (self.f(self.a, *self.nilai_var) + self.f(self.b, *self.nilai_var) + 4 * jumlah_ganjil + 2 * jumlah_genap)
        return integral, h

    def kaidah_simpson_3_8(self):
        if self.n % 3 != 0:
            raise ValueError("Nilai n harus merupakan kelipatan dari 3")
        h = (self.b - self.a) / self.n
        jumlah_3 = 0
        jumlah_sisa = 0
        for i in range(1, self.n):
            xi = self.a + i * h
            if i % 3 == 0:
                jumlah_3 += self.f(xi, *self.nilai_var)
            else:
                jumlah_sisa += self.f(xi, *self.nilai_var)
        integral = (3 * h / 8) * (self.f(self.a, *self.nilai_var) + self.f(self.b, *self.nilai_var) + 2 * jumlah_3 + 3 * jumlah_sisa)
        return integral, h
    
    def interpolasi_newton_cotes(self):
        x_interp = np.linspace(self.a, self.b, self.n + 1)
        y_interp = self.f(x_interp, *self.nilai_var)

        coef = np.zeros(self.n + 1)
        for i in range(self.n + 1):
            coef[i] = y_interp[i]
            for j in range(i):
                coef[i] = (coef[i] - coef[j]) / (x_interp[i] - x_interp[j])

        def interpolasi(x):
            hasil = 0
            for i in range(self.n + 1):
                term = coef[i]
                for j in range(i):
                    term *= (x - x_interp[j])
                hasil += term
            return hasil
        
        return interpolasi

    def plotting_fungsi_dan_area(self, h, metode):
        x = np.linspace(self.a, self.b, 1000)
        y = self.f(x, *self.nilai_var)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'b', label='f(x)')

        interpolasi = self.interpolasi_newton_cotes()
        y_interp = interpolasi(x)
        plt.plot(x, y_interp, 'r--', label='Polinom Interpolasi Newton-Cotes')
        
        if metode == 'trapesium':
            x_rect = np.linspace(self.a, self.b, self.n + 1)
            y_rect = self.f(x_rect, *self.nilai_var)
            for i in range(self.n):
                plt.fill([x_rect[i], x_rect[i], x_rect[i+1], x_rect[i+1]], [0, y_rect[i], y_rect[i+1], 0], 'b', edgecolor='r', alpha=0.2)
        elif metode == 'simpson_1_3':
            x_rect = np.linspace(self.a, self.b, self.n + 1)
            for i in range(0, self.n, 2):
                x_segment = np.linspace(x_rect[i], x_rect[i+2], 100)
                plt.fill_between(x_segment, self.f(x_segment, *self.nilai_var), alpha=0.2, color='b', edgecolor='r')
        elif metode == 'simpson_3_8':
            x_rect = np.linspace(self.a, self.b, self.n + 1)
            for i in range(0, self.n, 3):
                x_segment = np.linspace(x_rect[i], x_rect[i+3], 100)
                plt.fill_between(x_segment, self.f(x_segment, *self.nilai_var), alpha=0.2, color='b', edgecolor='r')
        
        plt.title(f"Integrasi menggunakan Kaidah {metode.replace('_', ' ').title()}")
        plt.xlabel('x')
        plt.ylabel('y = f(x)')
        plt.legend()
        plt.grid(True)
        plt.show()

def main():
    x = sp.symbols('x')
    
    while True:
        print("Pilih metode:")
        print("1. Kaidah Trapesium")
        print("2. Kaidah Simpson 1/3")
        print("3. Kaidah Simpson 3/8")
        pilihan = int(input("Masukkan pilihan: "))
        
        a = float(input("Masukkan nilai a: "))
        b = float(input("Masukkan nilai b: "))
        n = int(input("Masukkan jumlah segmen n: "))
        
        fungsi_str = input("Masukkan fungsi f(x, ...): ")
        try:
            fungsi_expr = sympify(fungsi_str)
            variabel = sorted(fungsi_expr.free_symbols, key=lambda s: s.name)
            if x not in variabel:
                print("Fungsi harus mengandung variabel x.")
                continue
            variabel.remove(x)
            nilai_var = []
            for var in variabel:
                val = float(input(f"Masukkan nilai untuk {var}: "))
                nilai_var.append(val)
        except (sp.SympifyError, TypeError) as e:
            print(f"Fungsi tidak valid: {e}")
            print("Pastikan Anda memasukkan fungsi dengan benar. Contoh yang benar: (4*x - x*3)*exp(t*2)")
            continue
        
        integrator = IntegrasiNumerik(fungsi_str, a, b, n, variabel, nilai_var)
        
        try:
            if pilihan == 1:
                hasil, h = integrator.kaidah_trapesium()
                print(f"Hasil dengan Kaidah Trapesium: {hasil}")
                integrator.plotting_fungsi_dan_area(h, 'trapesium')
            elif pilihan == 2:
                hasil, h = integrator.kaidah_simpson_1_3()
                print(f"Hasil dengan Kaidah Simpson 1/3: {hasil}")
                integrator.plotting_fungsi_dan_area(h, 'simpson_1_3')
            elif pilihan == 3:
                hasil, h = integrator.kaidah_simpson_3_8()
                print(f"Hasil dengan Kaidah Simpson 3/8: {hasil}")
                integrator.plotting_fungsi_dan_area(h, 'simpson_3_8')
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                continue
        except ValueError as e:
            print(e)
            continue
        
        break

if __name__ == "__main__":
    main()
    