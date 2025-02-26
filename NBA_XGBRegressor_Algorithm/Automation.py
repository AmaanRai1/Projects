import subprocess


basketball_script = "/Users/amaanrai/Desktop/BasketballBetting/Basketball_Reference_Player_Game_Log_Scraping.py"
defense_script = "/Users/amaanrai/Desktop/BasketballBetting/DefenseStats.py"
r_script = "/Users/amaanrai/Desktop/BasketballBetting/Cleaning_Data_v2.R"

try:
    print("Running Basketball Reference Scraper...")
    subprocess.run(["python3", basketball_script], check=True)

    print("Running Defense Stats Script...")
    subprocess.run(["python3", defense_script], check=True)

    print("Running Cleaning Data in R...")
    subprocess.run(["Rscript", r_script], check=True)

    print("All scripts executed successfully.")

except subprocess.CalledProcessError as e:
    print(f"Error encountered: {e}")
