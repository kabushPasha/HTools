import sys,os

target_dir = sys.argv[1]
src_html = os.path.dirname(__file__) + "/HTML_AutoGal.html"

# Create Files STRING
files = [f for f in os.listdir(target_dir) if os.path.isfile(target_dir + "/" + f)]
files_str = ""
for file in files:
	files_str += file + "\n"

target_name = os.path.basename(target_dir)

with open(src_html, "r") as f:
	old = f.read()
	old = old.replace("REPLACE_PATH", target_name + "/")
	old = old.replace("REPLACE_LIST", files_str)
	

out_html = target_dir + ".html"

with open(out_html, 'w') as f:
    f.write(old)