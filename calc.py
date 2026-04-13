import tkinter as tk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime
import os

class YapiGraphCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("Yapi Graph Calc V4.6 - TRACER OK")
        self.root.geometry("900x700")
        self.root.configure(bg="#2C3E50")
        
        self.expression = ""
        self.memoire = 0
        self.historique = []
        self.ans = 0
        self.clavier_ouvert = False
        self.fichier_notes = "notes_yapi.txt"
        
        self.creer_interface()
        
    def creer_interface(self):
        # Zone d'affichage
        self.affichage = tk.Entry(self.root, font=('Arial', 24, 'bold'), 
                                 justify='right', bd=10, relief='sunken',
                                 bg='white', fg='black')
        self.affichage.grid(row=0, columnspan=6, sticky="nsew", padx=5, pady=5)
        
        # Configuration grille
        for i in range(10):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.root.grid_columnconfigure(i, weight=1)
        
        boutons = [
            'LOG', '10^x', 'LN', 'EXP', 'e', 'π',
            'SIN', 'COS', 'TAN', 'nCr', 'nPr', 'RAND',
            '√', '^', 'x', '(', ')', 'ANS',
            'ABS', 'FACT', 'MOD', 'C', '⌫', '/',
            'STO', 'TRACER', '7', '8', '9', '*',
            'CLAVIER', 'SAUVE', '4', '5', '6', '-',
            'VOIR NOTES', 'ESPACE', '1', '2', '3', '+',
            'EFF NOTE', '(', ')', '0', '.', '='
        ]
        
        ligne = 1
        colonne = 0
        for bouton in boutons:
            if bouton == 'C':
                couleur = "#E74C3C"
            elif bouton == '=':
                couleur = "#27AE60"
            elif bouton == 'TRACER':
                couleur = "#9B59B6"
            elif bouton in ['SAUVE', 'VOIR NOTES', 'EFF NOTE']:
                couleur = "#16A085"
            elif bouton == 'CLAVIER':
                couleur = "#F39C12"
            elif bouton in ['0','1','2','3','4','5','6','7','8','9','.']:
                couleur = "#3498DB"
            elif bouton in ['+','-','*','/','^','x']:
                couleur = "#E67E22"
            else:
                couleur = "#34495E"
                
            cmd = lambda x=bouton: self.clic_bouton(x)
            
            tk.Button(self.root, text=bouton, font=('Arial', 12, 'bold'),
                     bg=couleur, fg='white', bd=3, relief='raised',
                     command=cmd).grid(row=ligne, column=colonne, 
                     sticky="nsew", padx=2, pady=2)
            
            colonne += 1
            if colonne > 5:
                colonne = 0
                ligne += 1
    
    def clic_bouton(self, valeur):
        try:
            if valeur == 'C':
                self.expression = ""
            elif valeur == '⌫':
                self.expression = self.expression[:-1]
            elif valeur == '=':
                self.calculer()
            elif valeur == 'ANS':
                self.expression += str(self.ans)
            elif valeur == 'STO':
                self.memoire = float(eval(self.expression))
                messagebox.showinfo("Mémoire", f"Valeur {self.memoire} stockée")
            elif valeur == 'RAND':
                self.expression += str(np.random.random())
            elif valeur == 'TRACER':
                self.tracer_fonction()
            elif valeur == 'CLAVIER':
                self.basculer_clavier()
            elif valeur == 'SAUVE':
                self.sauver_note()
            elif valeur == 'VOIR NOTES':
                self.voir_notes()
            elif valeur == 'EFF NOTE':
                self.effacer_notes()
            elif valeur == 'ESPACE':
                self.expression += " "
            elif valeur == 'π':
                self.expression += str(math.pi)
            elif valeur == 'e':
                self.expression += str(math.e)
            elif valeur == '√':
                self.expression += 'sqrt('
            elif valeur == '^':
                self.expression += '^'
            elif valeur == 'LOG':
                self.expression += 'log10('
            elif valeur == 'LN':
                self.expression += 'log('
            elif valeur == '10^x':
                self.expression += '10**'
            elif valeur == 'EXP':
                self.expression += 'exp('
            elif valeur == 'SIN':
                self.expression += 'sin('
            elif valeur == 'COS':
                self.expression += 'cos('
            elif valeur == 'TAN':
                self.expression += 'tan('
            elif valeur == 'ABS':
                self.expression += 'abs('
            elif valeur == 'FACT':
                self.expression += 'factorial('
            elif valeur == 'MOD':
                self.expression += '%'
            elif valeur == 'nCr':
                self.expression += 'comb('
            elif valeur == 'nPr':
                self.expression += 'perm('
            else:
                self.expression += str(valeur)
                
            self.affichage.delete(0, tk.END)
            self.affichage.insert(0, self.expression)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")
    
    def calculer(self):
        try:
            # On ne remplace PLUS x par * car x = variable
            expr = self.expression.replace('^', '**')
            expr = expr.replace('sin(', 'math.sin(math.radians(')
            expr = expr.replace('cos(', 'math.cos(math.radians(')
            expr = expr.replace('tan(', 'math.tan(math.radians(')
            expr = expr.replace('log10(', 'math.log10(')
            expr = expr.replace('log(', 'math.log(')
            expr = expr.replace('exp(', 'math.exp(')
            expr = expr.replace('sqrt(', 'math.sqrt(')
            expr = expr.replace('abs(', 'abs(')
            expr = expr.replace('factorial(', 'math.factorial(')
            expr = expr.replace('comb(', 'math.comb(')
            expr = expr.replace('perm(', 'math.perm(')
            
            resultat = eval(expr)
            self.ans = resultat
            self.historique.append(f"{self.expression} = {resultat}")
            self.expression = str(resultat)
            self.affichage.delete(0, tk.END)
            self.affichage.insert(0, self.expression)
            
        except Exception as e:
            messagebox.showerror("Erreur", "Expression invalide")
            self.expression = ""
    
    def tracer_fonction(self):
        try:
            expr = self.affichage.get()
            if not expr:
                messagebox.showwarning("Attention", "Entre une fonction avec x")
                return
                
            fenetre_graph = tk.Toplevel(self.root)
            fenetre_graph.title(f"Graphique : y = {expr}")
            fenetre_graph.geometry("800x600")
            
            fig, ax = plt.subplots(figsize=(8, 6))
            x = np.linspace(-10, 10, 1000)
            
            # On ne remplace PLUS x par * car x = variable
            expr_np = expr.replace('^', '**')
            expr_np = expr_np.replace('sin(', 'np.sin(np.radians(')
            expr_np = expr_np.replace('cos(', 'np.cos(np.radians(')
            expr_np = expr_np.replace('tan(', 'np.tan(np.radians(')
            expr_np = expr_np.replace('log10(', 'np.log10(')
            expr_np = expr_np.replace('log(', 'np.log(')
            expr_np = expr_np.replace('exp(', 'np.exp(')
            expr_np = expr_np.replace('sqrt(', 'np.sqrt(')
            expr_np = expr_np.replace('abs(', 'np.abs(')
            
            y = eval(expr_np)
            
            ax.plot(x, y, 'b-', linewidth=2)
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f'y = {expr}')
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            
            canvas = FigureCanvasTkAgg(fig, fenetre_graph)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Erreur Graphique", f"Impossible de tracer : {str(e)}")
    
    def basculer_clavier(self):
        if not self.clavier_ouvert:
            self.clavier_ouvert = True
            self.fenetre_clavier = tk.Toplevel(self.root)
            self.fenetre_clavier.title("Clavier AZERTY")
            self.fenetre_clavier.geometry("700x250")
            self.fenetre_clavier.configure(bg="#2C3E50")
            self.fenetre_clavier.protocol("WM_DELETE_WINDOW", self.fermer_clavier)
            
            touches = [
                ['A','Z','E','R','T','Y','U','I','O','P'],
                ['Q','S','D','F','G','H','J','K','L','M'],
                ['W','X','C','V','B','N','⌫','EFF']
            ]
            
            for i, ligne in enumerate(touches):
                frame = tk.Frame(self.fenetre_clavier, bg="#2C3E50")
                frame.pack(pady=5)
                for touche in ligne:
                    if touche == '⌫':
                        cmd = lambda: self.touche_clavier('BACK')
                    elif touche == 'EFF':
                        cmd = lambda: self.touche_clavier('EFF')
                    else:
                        cmd = lambda t=touche: self.touche_clavier(t)
                    
                    tk.Button(frame, text=touche, font=('Arial', 14, 'bold'),
                             width=3, height=2, bg="#34495E", fg='white',
                             command=cmd).pack(side=tk.LEFT, padx=2)
        else:
            self.fermer_clavier()
    
    def fermer_clavier(self):
        self.clavier_ouvert = False
        self.fenetre_clavier.destroy()
    
    def touche_clavier(self, touche):
        if touche == 'BACK':
            self.expression = self.expression[:-1]
        elif touche == 'EFF':
            self.expression = ""
        else:
            self.expression += touche.lower()
        
        self.affichage.delete(0, tk.END)
        self.affichage.insert(0, self.expression)
    
    def sauver_note(self):
        texte = self.affichage.get()
        if not texte:
            messagebox.showwarning("Attention", "Rien à sauvegarder")
            return
        
        with open(self.fichier_notes, "a", encoding="utf-8") as f:
            date = datetime.now().strftime("%d/%m/%Y %H:%M")
            f.write(f"[{date}] {texte}\n")
        
        messagebox.showinfo("Sauvegardé", "Note enregistrée !")
        self.expression = ""
        self.affichage.delete(0, tk.END)
    
    def voir_notes(self):
        if not os.path.exists(self.fichier_notes):
            messagebox.showinfo("Notes", "Aucune note pour le moment")
            return
        
        fenetre_notes = tk.Toplevel(self.root)
        fenetre_notes.title("Mes Notes YapiGraphCalc")
        fenetre_notes.geometry("600x400")
        
        texte = tk.Text(fenetre_notes, font=('Arial', 12), wrap=tk.WORD)
        texte.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        with open(self.fichier_notes, "r", encoding="utf-8") as f:
            contenu = f.read()
            texte.insert(tk.END, contenu)
        
        texte.config(state=tk.DISABLED)
    
    def effacer_notes(self):
        if messagebox.askyesno("Confirmation", "Effacer toutes les notes ?"):
            if os.path.exists(self.fichier_notes):
                os.remove(self.fichier_notes)
            messagebox.showinfo("Fait", "Notes effacées")

if __name__ == "__main__":
    root = tk.Tk()
    app = YapiGraphCalc(root)
    root.mainloop()