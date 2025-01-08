import nmap
from rich.console import Console
import whois
import socket
import os

console = Console()
nm = nmap.PortScanner()

def main():
    global target
    results = []  # Глобальний список для всіх результатів
    target = console.input("[green]Enter the target (domain/ip): ").strip()

    try:
        # Перевіряємо та отримуємо IP-адресу
        ip_address = socket.gethostbyname(target)
        console.print(f"[green]Resolved IP: [yellow]{ip_address}")
    except socket.gaierror:
        console.print(f"[red]Unable to resolve target: {target}")
        return

    console.print(f"[green]Scanning host: [red]{target}...")

    try:
        nm.scan(ip_address, arguments='-sV', timeout=60)
        results.append(f"Scanning host: {target} ({ip_address})")

        # Зчитуємо відкриті порти
        for port in nm[ip_address]['tcp']:
            service = nm[ip_address]['tcp'][port]['name']
            results.append(f"Port {port}: {service}")
            console.print(f"[green]Port {port}: [red]{service}")

    except Exception as e:
        console.print(f"[red]Error during scanning: {e}")
        return

    save_results(results, "Port and Service Scan Results")
    eyes(ip_address, results)  # Переходимо до аналізу WHOIS

def eyes(ip_address, results):
    console.print("[green]Start WHOIS analysis? [1 - Yes, 2 - No]")
    if int(input(": ")) == 1:
        try:
            w = whois.whois(target)
            results.append("WHOIS Analysis Results:")

            # Додаємо всі ключі WHOIS-результатів у список
            for key, value in w.items():
                results.append(f"{key}: {value}")
                console.print(f"[green]{key}: [yellow]{value}")
        except Exception as e:
            console.print(f"[red]Error during WHOIS analysis: {e}")

    save_results(results, "WHOIS Analysis Results")
    os_scan(ip_address, results)  # Переходимо до аналізу ОС

def os_scan(ip_address, results):
    console.print("[green]Scanning OS on target IP...")

    # Перевірка, чи виконується скрипт з правами адміністратора
    if os.name == 'nt' and not os.environ.get("USERDOMAIN"):
        console.print("[red]OS detection requires administrator privileges. Run the script as admin.")
        return

    try:
        nm.scan(ip_address, arguments='-O', timeout=60)
        results.append("OS Detection Results:")

        if 'osmatch' in nm[ip_address]:
            for os_match in nm[ip_address]['osmatch']:
                results.append(f"- OS Name: {os_match['name']} (Accuracy: {os_match['accuracy']}%)")
                console.print(f"[green]- OS Name: [yellow]{os_match['name']} [green](Accuracy: {os_match['accuracy']}%)")
        else:
            results.append("No OS information detected.")
            console.print("[red]No OS information detected.")
    except Exception as e:
        console.print(f"[red]Error during OS scanning: {e}")

    save_results(results, "OS Detection Results")
    console.print("[green]Scanning complete!")

def save_results(results, section_title):
    """
    Зберігає результати в один файл з додаванням нового розділу.
    """
    # Перевіряємо існування папки Results
    folder_name = "Results"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Вказуємо шлях до файлу
    file_name = os.path.join(folder_name, f"results_{target}.txt")
    try:
        with open(file_name, "a") as file:
            file.write("\n" + "#" * 30 + f"\n{section_title}\n" + "#" * 30 + "\n")
            file.write("\n".join(results) + "\n")
        console.print(f"[green]Results saved to [yellow]{file_name}")
        results.clear()  # Очищуємо список після збереження
    except Exception as e:
        console.print(f"[red]Error saving results: {e}")

if __name__ == '__main__':
    main()
