from openai_helpers import create_content
from prompts import get_prompts

(counter, prompt_file_name, output_file_name) = get_prompts(1)
print(counter, " > ", prompt_file_name, " > ", output_file_name)
create_content(counter, prompt_file_name, output_file_name)