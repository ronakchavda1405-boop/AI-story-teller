
# ==========================================
# AI STORY TELLER - STREAMLIT UI
# ==========================================

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# STEP 1: Page configuration

st.set_page_config(
    page_title="AI Story Teller",
    page_icon="📖",
    layout="centered"
)

# STEP 2: Load API key from .env

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# STEP 3: Genre-based temperature

genre_temperature = {
    "Horror": 0.9,
    "Comedy": 0.9,
    "Romance": 0.8,
    "Adventure": 0.9,
    "Mystery": 0.5,
    "Science Fiction": 0.8,
    "Fantasy": 0.9,
    "Drama": 0.7,
    "Thriller": 0.7,
    "Crime": 0.5
}

# STEP 4: Story length dictionary

story_lengths = {
    "Short": "200-300 words",
    "Medium": "500-700 words",
    "Long": "1000-1500 words"
}

# STEP 5: UI Design

st.title("📖 AI Story Teller")

st.write(
    "Welcome to AI Story Teller! "
    "Create your own unique story using Artificial Intelligence."
)

st.divider()

# STEP 6: Take inputs from user

st.subheader("✨ Create Your Story")

topic = st.text_input(
    "Enter Your Story Topic",
    placeholder="Example: A lost astronaut on Mars"
)

genre = st.selectbox(
    "Choose Story Genre",
    [
        "Horror",
        "Comedy",
        "Romance",
        "Adventure",
        "Mystery",
        "Science Fiction",
        "Fantasy",
        "Drama",
        "Thriller",
        "Crime"
    ]
)

length = st.selectbox(
    "Choose Story Length",
    ["Short", "Medium", "Long"]
)

# STEP 7: Display selected temperature

temperature = genre_temperature[genre]

st.info(
    f"Selected Genre: {genre} | "
    f"Temperature: {temperature}"
)

# STEP 8: Generate Story button


# STEP 8: Generate Story button

if st.button("🚀 Generate My Story", use_container_width=True):

    # Validate topic
    if not topic.strip():

        st.warning(
            "Please enter a story topic as required."
            
        )

    # Validate topic length
    elif len(topic.strip()) < 3:

        st.warning(
            "Please enter a meaningful story topic "
            "with at least 3 characters."
        )

    # Validate genre
    elif genre.title() not in genre_temperature:

        st.warning(
            "Please select a valid story genre."
        )

    # Validate story length
    elif length.title() not in story_lengths:

        st.warning(
            "Please select story length as Short, Medium or Long."
        )

    else:

        # Convert inputs into lowercase
        topic = topic.lower().strip()
        genre = genre.lower().strip()
        length = length.lower().strip()

        # Select temperature according to genre
        temperature = genre_temperature[genre.title()]

        # Select story word count
        word_count = story_lengths[length.title()]

        # Create story prompt
        story_prompt = f"""
        You are a professional creative storyteller.

        Generate a creative and engaging story.

        Story Topic: {topic}
        Story Genre: {genre}
        Story Length: {word_count}

        Instructions:
        1. Follow the selected genre.
        2. Create interesting characters.
        3. Include a beginning, middle and ending.
        4. Follow the requested word count.
        5. Give the story an attractive title.
        6. Return only the story.
        """

        try:

            client = Groq(api_key=api_key)

            with st.spinner("AI is writing your story..."):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "user",
                            "content": story_prompt
                        }
                    ],
                    temperature=temperature,
                    max_completion_tokens=3000
                )

                story = response.choices[0].message.content

            if story:
                st.success("Your story is ready!")
                st.subheader("📚 Your AI Generated Story")
                st.markdown(story)

                st.download_button(
                    label="⬇️ Download Your Story",
                    data=story,
                    file_name="my_ai_story.txt",
                    mime="text/plain"
                )
            else:
                st.warning("Sorry, no story was generated. Please try again.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")


st.divider()

st.caption("Powered by Groq LLM | Built with Python & Streamlit")
