# Théorème de Yaglom

## Lemme admis
Si $E[Z_1] = 1$ et $Var[Z_1] < +\infty$ alors,  

$$
\lim_{n \to +\infty} \frac{1}{n} * (\frac{1}{1-f_n(t)} - \frac{1}{1-t}) = \frac{\sigma^2}{2}
, \hspace{8px} \forall t \in [0, 1[
$$

### Corollaire : équivalent de $P(Z_n > 0)$ quand $n \to +\infty$

En évaluant l'égalité du lemme en $t=0$, on obtient

$$ \lim_{n \to +\infty} \frac{1}{n} * (\frac{1}{1-f_n(0)}) - \frac{1}{n} = \frac{\sigma^2}{2}
$$

Comme $\displaystyle \lim_{n \to +\infty} \frac{1}{n} = 0$, on a alors

$$ (\frac{1}{1-f_n(0)}) \sim \frac{n * \sigma^2}{2}
$$

c'est à dire

$$ 1-f_n(0) \sim \frac{2}{n * \sigma^2}
$$

ou encore

$$ P(Z_n > 0) \sim \frac{2}{n * \sigma^2}
$$

## Vitesse de divergence de $E[Z_n | Z_n > 0]$
Le corollaire peut nous donner une idée de la vitesse de divergence du processus $Z_n | Z_n > 0$.

$$
\begin{align*}
    E[Z_n | Z_n > 0] &= \sum_{k=0}^{+\infty} k * P(Z_n = k | Z_n > 0)
    \hspace{10px} \text{par définition de l'espérance} \\
    &= \sum_{k=0}^{+\infty} k * \frac{P(Z_n = k \cap Z_n > 0)}{P(Z_n > 0)} \hspace{10px} \text{en utilisant la formule de Bayes}\\
\end{align*}
$$

Or $\hspace{10px} P(Z_n = k \cap Z_n > 0) = P(Z_n = k), \forall k \ge 1$  
et, pour $\hspace{4px} k=0, \hspace{6px} 0 * P(Z_n = 0 \cap Z_n > 0) = 0 * P(Z_n = 0)$  
d'où $\hspace{6px} \displaystyle \sum_{k=0}^{+\infty} k * P(Z_n = k \cap Z_n > 0) = \sum_{k=0}^{+\infty} k * P(Z_n = k)$  
Ce qui nous donne 

$$
\begin{align*}
    E[Z_n | Z_n > 0] &= \frac{1}{P(Z_n > 0)} \sum_{k=0}^{+\infty} k * P(Z_n = k) \\
    &= \frac{E[Z_n]}{P(Z_n > 0)} \\
    &= \frac{m^n}{P(Z_n > 0)} \\
    &= \frac{1}{P(Z_n > 0)}
\end{align*}
$$

Car nous sommes dans le cas critique où $m=1$.  

Finalement, grâce au corollaire on obtient immédiatement que $E[Z_n | Z_n > 0] \sim \frac{n * \sigma^2}{2}$

## Théorème de Yaglom
Comme la moyenne du processus conditionné $Z_n | Z_n > 0$ diverge à la même vitesse que $n$, il vient l'idée de diviser ce processus par un facteur $n$. De la sorte, nous pourrons tomber sur un processus qui converge vers une loi exponentielle de paramètre $\frac{2}{\sigma^2}$.  

Ce résultat est donné par le théorème de Yaglom :  

Si $E[Z_1] = 1$ et $Var[Z_1] = \sigma^2 < +\infty$ alors, 

$$ \lim_{n \to +\infty} P(\frac{Z_n}{n} > z | Z_n > 0) = \exp{(\frac{-2 z}{\sigma^2})}, \hspace{10px} \forall z \ge 0
$$

### Démonstration
#### Problème auxiliaire
En utilisant les transformées de Laplace, on admet qu'il suffit de démontrer l'égalité suivante :

$$ \lim_{n \to +\infty} E[\exp{(-\alpha * \frac{Z_n}{n})} | Z_n > 0]
    = \frac{1}{1 + \frac{\alpha \sigma^2}{2}}
$$

En effet, on peut retrouver la partie droite de l'égalité en écrivant la transformée de Laplace de $\exp{(\frac{-2 z}{\sigma^2})}$ :

$$ \begin{align*}
    \mathcal{L}(\exp{(\frac{-2 z}{\sigma^2})})
        &= \frac{1}{\alpha + \frac{2}{\sigma^2}} \\
        &= \frac{2}{2 + \alpha \sigma^2} \\
        &= \frac{1}{1 + \frac{\alpha \sigma^2}{2}}
\end{align*}
$$

La partie gauche de l'égalité peut être retrouvée en utilisant la transformée de Laplace pour une variable aléatoire :

$$\begin{align*}
\mathcal{L}_{X} : & \hspace{6px} \mathbb{R} \to \mathbb{R} \\
      & \hspace{6px} t \to \mathbb{E}[e^{tX}]
\end{align*}
$$

Par identification, il faut prendre $\mathcal{L}_{\frac{Z_n}{n}}(- \alpha)$.  
Cependant, je ne sais pas expliquer comment le passage par ces transformées conserve l'égalité.

#### Résolution du problème auxiliaire
Partont de la partie gauche de l'égalité.  
On admet le résultat suivant :

$$E[\exp{(-\alpha * \frac{Z_n}{n})} | Z_n > 0] = \frac{f_n(\mathbb{e^{-\alpha / n}}) - f_n(0)}{1 - f_n{0}}
$$

On peut réécrire la partie de droite sous une forme qui fait apparaître le résultat du corollaire :

$$ \begin{align*}
\frac{f_n(\mathbb{e^{-\alpha / n}}) - f_n(0)}{1 - f_n{0}}
    &= \frac{1 - f_n(0) - (1 - f_n(\mathbb{e^{-\alpha / n}}))}{1 - f_n{0}} \\
    &= 1 - \frac{1 - f_n(\mathbb{e^{-\alpha / n}})}{1 - f_n{0}} \\
    &= 1 - \frac{[n * (1 - f_n(\mathbb{e^{-\alpha / n}}))]^{-1}}{[n * (1 - f_n{0})]^{-1}}
\end{align*}
$$

On sait, par le corollaire du lemme, que
$\displaystyle \lim_{n \to +\infty} \frac{1}{n} * (\frac{1}{1-f_n(0)}) = \frac{\sigma^2}{2}$.  

Par ailleurs, en utilisant la convergence uniforme, on a
$
\displaystyle \lim_{n \to +\infty} \frac{1}{n(1-f_n(e^{-\alpha / n}))}
= \frac{\sigma^2}{2} + \lim_{n \to +\infty} \frac{1}{n(1-e^{-\alpha / n})}
= \frac{\sigma^2}{2} + \frac{1}{\alpha}
$.  

Finalement, en passant à la limite, on a :

$$
\begin{align*}
\lim_{n \to +\infty} E[\exp{(-\alpha * \frac{Z_n}{n})} | Z_n > 0]
    &= 1 - \frac{\frac{\sigma^2}{2}}{\frac{\sigma^2}{2} + \frac{1}{\alpha}} \\
    &= 1 - \frac{1}{1 + \frac{2}{\alpha \sigma^2}}
    \hspace{10px} \text{en factorisant par $\sigma^2 / 2$} \\
    &= 1 - \frac{\alpha \sigma^2}{\alpha \sigma^2 + 2} \\
    &= \frac{2}{\alpha \sigma^2 + 2} \\
    &= \frac{1}{\frac{\alpha \sigma^2}{2} + 1}
\end{align*}
$$

Et on trouve bien le membre de droite de l'égalité auxiliaire que nous cherchions à démontrer.
