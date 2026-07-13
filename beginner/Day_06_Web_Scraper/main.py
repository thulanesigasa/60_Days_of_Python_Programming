import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
import csv
import os
import threading

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 6: Web Scraper")
        self.root.geometry("550x520")
        self.root.configure(bg="#121212")  # 60% Black
        self.root.resizable(False, False)

        # Header Label
        self.header_label = tk.Label(
            self.root, 
            text="WEB DATA SCRAPER", 
            font=("Helvetica", 16, "bold"), 
            bg="#121212", 
            fg="#1E3A8A"  # 20% Cobalt Blue Accent
        )
        self.header_label.pack(pady=20)

        # Input Frame
        self.input_frame = tk.Frame(self.root, bg="#121212")
        self.input_frame.pack(fill="x", padx=30, pady=(0, 15))

        self.url_entry = tk.Entry(
            self.input_frame,
            font=("Helvetica", 11),
            bg="#1E293B",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            bd=0,
            relief="flat"
        )
        self.url_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.url_entry.insert(0, "https://news.ycombinator.com")

        self.scrape_btn = tk.Button(
            self.input_frame,
            text="Scrape",
            font=("Helvetica", 10, "bold"),
            bg="#1E3A8A",
            fg="#FFFFFF",
            activebackground="#2563EB",
            activeforeground="#FFFFFF",
            bd=0,
            padx=15,
            command=self.start_scraping,
            cursor="hand2"
        )
        self.scrape_btn.pack(side="right", ipady=6)

        # Text Console Log (Cobalt blue panel border, dark background)
        self.log_area = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 10),
            bg="#1E293B",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            bd=0,
            relief="flat"
        )
        self.log_area.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        self.log_area.insert(tk.END, "Log panel ready. Enter a URL above and click Scrape.\n")
        self.log_area.config(state="disabled")

    def log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def start_scraping(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL!")
            return
        
        self.scrape_btn.config(state="disabled")
        self.log(f"[*] Starting scrape process for: {url}")
        
        # Run scraping in background thread to keep GUI responsive
        threading.Thread(target=self.scrape_website, args=(url,), daemon=True).start()

    def scrape_website(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=6)
            if response.status_code != 200:
                self.log(f"[!] Server returned status code: {response.status_code}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to retrieve page: {response.status_code}"))
                return
            
            self.log("[*] Page content retrieved successfully. Parsing...")
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Scrape headings or hyperlinks depending on the site.
            title_nodes = soup.select(".titleline a")
            scraped_items = []
            
            if title_nodes:
                self.log(f"[*] Detected HackerNews elements. Extracting articles...")
                for node in title_nodes:
                    if "href" in node.attrs and not node["href"].startswith("from?site="):
                        scraped_items.append((node.get_text(), node["href"]))
            else:
                self.log("[*] Custom elements not found, parsing all <a> links...")
                for a in soup.find_all("a", href=True):
                    text = a.get_text().strip()
                    href = a["href"]
                    if text and href.startswith("http"):
                        scraped_items.append((text, href))

            if not scraped_items:
                self.log("[!] No extractable items found.")
                self.root.after(0, lambda: messagebox.showinfo("No Data", "No items could be extracted from this page."))
                return

            self.log(f"[+] Found {len(scraped_items)} data entries. Writing to CSV...")
            
            # Save to CSV in the same folder
            csv_path = os.path.join(os.path.dirname(__file__), "scraped_data.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Title/Label", "URL"])
                writer.writerows(scraped_items[:100])

            self.log(f"[+] Scraped data successfully exported to:\n    {csv_path}")
            
            # Print sample to console
            self.log("\n--- SCRAPED SAMPLE (Top 5) ---")
            for i, (title, href) in enumerate(scraped_items[:5], 1):
                self.log(f"{i}. {title[:50]}... \n   {href}")
            self.log("-------------------------------\n")
            
        except Exception as e:
            self.log(f"[!] Exception occurred: {e}")
            self.root.after(0, lambda: messagebox.showerror("Exception", f"An error occurred: {e}"))
        finally:
            self.root.after(0, lambda: self.scrape_btn.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
