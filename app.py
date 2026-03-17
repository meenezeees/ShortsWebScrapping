from playwright.sync_api import sync_playwright
from colorama import Fore
import re

base_url = "https://www.youtube.com/@StetchShorts"

def ascii_confirmation():
    with open("C:/Users/AMD/Documents/Projetos VScode/ShortsWebScrapping/TxtFiles/ascii.txt", "r") as art:
                ascii_art = art.read()

    print(Fore.GREEN + ascii_art + Fore.RESET)

with sync_playwright() as p:
    browser = p.chromium.launch(
         headless = True
    )

    context = browser.new_context(
        viewport = {"width":600, "height":720}
    )

    def get_urls():
        links_page = context.new_page()
        links_page.goto(base_url)

        hrefs = links_page.eval_on_selector_all(
             "a[href*='/shorts/']",
             "elements => elements.map(e => e.href)"
    )
        fixed_hrefs = list(set(hrefs))

        with open("C:/Users/AMD/Documents/Projetos VScode/ShortsWebScrapping/TxtFiles/links.txt", "w") as url:
            url.write("\n".join(fixed_hrefs))

        ascii_confirmation()
        print(Fore.LIGHTBLUE_EX + "\nLinks atualizados.\n" + Fore.RESET)

        links_page.close()

    def next_video():
        page.goto(next(it))

    def get_content():
        current_url = page.url
        watch_url = current_url.replace("shorts/", "watch?v=")

        page.goto(watch_url)
        more_button = page.get_by_text("more")

        html = page.content()
        match = re.search(r'"attributedDescription":\{"content":"(.*?)"\}', html)

        if match:
            texto = match.group(1)
            
            raw = texto

            clean = raw.split('","commandRuns"')[0]
            clean = clean.strip('"')
            clean = clean

            with open("C:/Users/AMD/Documents/Projetos VScode/ShortsWebScrapping/TxtFiles/descricao.txt", "a") as f:
                f.write("\n" + clean.splitlines()[0] + "\n")

                ascii_confirmation()
                print(Fore.LIGHTBLUE_EX + "\nDescrições atualizadas\n" + Fore.RESET)

    get_urls()

    lista = [linha.strip() for linha in open("C:/Users/AMD/Documents/Projetos VScode/ShortsWebScrapping/TxtFiles/links.txt", "r", encoding = "utf-8") if linha.strip()]
    it = iter(lista)

    page = context.new_page()
    page.goto(next(it))

    contador = 0
    while contador < 5:
        get_content()
        next_video()

        contador += 1

        print("{}/5".format(contador))

    browser.close()