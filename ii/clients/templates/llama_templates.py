SEGMENT_GENERATION_TEMPLATE = """
You are working with a human to create a story in the style of choose your own adventure.

The human is playing the role of the protaganist in the story which you are tasked to
help write. To create the story, we do it in steps, where each step produces a STORYBLOCK.
Each STORYBLOCK consists of a CONTENT, a set of CHOICES that the protaganist can take, and the
chosen CHOICE. The story will have a total of {story_length} STORYBLOCKs. There are 
currently NUM_BLOCKS = {num_blocks}. The genre is {genre}.

Below we attach the history of the adventure so far.

PREVIOUS STORYBLOCKs:
---
{story}

If there are no previous STORYBLOCKs (i.e. NUM_BLOCKS == 0), generate an initial plot. Then take 
that initial plot and characters and start over. DO NOT REUSE ANYTHING. Give the 
protaganist a name and an interesting challenge to solve.

Continue the story by generating the next block's CONTENT and set of CHOICES. 


Use the provided data model to structure your output.

This will be the last STORYBLOCK? {last_block}. If YES, wrap up the story in the next block (do not provide any choices). 
"""

INITIAL_IMAGE_TEMPLATE = """
Generate an image based on the below plot scene. Choose an artistic style of any type but make sure to depict the setting, 
characters, and what they are doing. Do NOT include text in the generated image.

{story}
"""

IMAGE_TEMPLATE = """
Generate an image for a story based on the plot scene below. This image is not the first in the story and so the art style and 
imagery should be as close to the previous image as possible. Do NOT include text in the generated image.

===
Previous styles: {previous_styles}

===
Previous descriptions: {previous_descriptions}

===
{current_scene_description}
"""

IMAGE_DESCRIPTION_TEMPLATE = """
You are tasked with describing the image below. Give a description of the image and describe its artistic style. 
Make sure to accurately describe the setting, characters, and what they are doing.

If a main character is in the image then be sure to fully describe what they look like.

Also, be sure to be as descriptive as possible with the artistic style -- make it so that a future artist could create a similar image with the exact same description.

It was created with the story content: {story}. Image URL: {image_url}
"""
