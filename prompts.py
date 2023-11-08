PROMPT_EMAIL = [
                    {
                        "type": "system",
                        "content": "You are a email content generation system which is tasked to generating a engaging short and crisp email given the context. You have to provide me with a email content which is catchy and crisp. It should be in less than 1000 words. Please provide only the Subject, Title and Body in the output JSON"
                    },
                    {
                        "type": "human",
                        "content": """The context is as follow: {info}"""
                    },
                    {
                    "type": "human",
                    "content": "Please provide me the email inside a JSON BLOB"
                    }
                ]

PROMPT_WHATSAPP = [
                    {
                        "type": "system",
                        "content": "You are a whatsapp content generation system which is tasked to generating a engaging whatsapp promotion content given the context. You have to provide me with a whatsapp content which is catchy. Keep it maximum 2500 characters. Only provide one key 'message' with the message in output JSON"
                    },
                    {
                        "type": "human",
                        "content": """Context: {info}"""
                    },
                    {
                    "type": "human",
                    "content": "Please provide me the message inside a JSON BLOB"
                    }
                ]

PROMPT_SMS = [
                    {
                        "type": "system",
                        "content": "You are a SMS content generation system which is tasked to generating a engaging SMS promotion content given the context. You have to provide me with a SMS content which is catchy. Keep it maximum 1600 characters. Only provide one key 'message' with the message in output JSON"
                    },
                    {
                        "type": "human",
                        "content": """Context: {info}"""
                    },
                    {
                    "type": "human",
                    "content": "Please provide me the message inside a JSON BLOB"
                    }
                ]
                
PROMPT_CARDS = [
                    {
                        "type": "system",
                        "content": "Provide the image generation prompt provided the context. The image generated should be in style of cards with the theme incorporating the information provided int the context.  What are main items associated with the ocassion and the industry and make the image be influenced by both of them. Please keep the colour selection and background in the theme of the event/ocassion."
                    },
                    {
                        "type": "human",
                        "content": """Context: {info}"""
                    },
                    {
                    "type": "human",
                    "content": "Please provide me the prompt inside a JSON BLOB with prompt as the key "
                    }
                ]

PROMPT_BANNER = [
                    {
                        "type": "system",
                        "content": "Provide the image generation prompt provided the user context"
                    },
                    {
                        "type": "human",
                        "content": """Context: {info}"""
                    },
                    {
                    "type": "human",
                    "content": "Please provide me the prompt inside a JSON BLOB with prompt as the key. Please specify not to include any human figure in the image. Also specify to not generate any text."
                    }
                ]
                
PROMPT_HOLIDAY = [
                    {
                        "type": "system",
                        "content": "Given a list of upcoming holidays, the industry of the company, and the region of the target audience, please recommend the top 3 festivals for a marketing campaign from the provided holiday list. Consider the cultural relevance and potential impact on the company's industry and target market. If there are multiple holidays in the list, prioritize the ones that align best with the company's goals. Do not add explanation, only provide JSON as output."
                    },
                    {
                        "type": "human",
                        "content": """Context: {info}"""
                    },
                    {
                        "type": "human",
                        "content": 'Only provide a JSON output with the key "top_holidays" containing the list of best holiday from the provided holiday list(Return the name as it is as it was in the context)'
                    }
                ]
                
PROMPT_HOLIDAY2 = [
                    {
                        "type": "system",
                        "content": "Given a list of upcoming holidays, the industry of the company, and the region of the target audience, please recommend the top 3 festivals for a marketing campaign from the provided holiday list. Consider the cultural relevance and potential impact on the company's industry and target market. If there are multiple holidays in the list, prioritize the ones that align best with the company's goals. Do not add explanation, only provide JSON as output."
                    },
                    {
                        "type": "human",
                        "content": """Context: {info}"""
                    },
                    {
                        "type": "human",
                        "content": """generate a JSON Response in following structure(Index in list always starts from 0):
                                    {"most_suited": "fill in the top 3 holiday names as a string that is most suited to run the marketing campaign also provide an argument why you picked these 3 over the rest", top_holidays": list containing the index of position of the top 3 holidays present in 'most_suited' in the original 'holidays' list}"""
                    }
                ]
                
PROMPT_PLANNER = [
                    {
                        "type": "system",
                        "content": "You are tasked with suggesting the best dates to run the marketing campaign for a given ocassion which is falling on a particular date (date of the ocassion is provided in YYYY-MM-DD format and also the name of of ocassion is provided) , also provide a short description of what the campaign goal will be for given date. Use your knowledge source in marketing to answer this question. Only provide dates with short description as output, give output in json format. Also make sure the goal is in line with the industry that the user is working in  which is also provided in the context"

                    },
                    {
                        "type": "human",
                        "content": """Context: {info}"""
                    },
                    {
                    "type": "human",
                    "content": "Only output a single JSON BLOB with the dates as keys(which should always be in YYYY-MM-DD format) and the values as the objective for that date. keep the objective under 10 words. Do not select more than 4 days."
                    }
                ]

PROMPT_PLANNER_V2 = [
                    {
                        "type": "system",
                        "content": "You are tasked with suggesting the best dates to run the marketing campaign given the prompt by marketer (you are also provided the today date in case the user does not specify the date use today date as the first date of planning, otherwise decipher from the user input in context when the event is occuring) , also provide a short description of what the campaign goal will be for given date. Use your knowledge source in marketing to answer this question. Only provide dates with short description as output, give output in json format. Also make sure the goal is in line with the industry that the user is working in  which is also provided in the context"

                    },
                    {
                        "type": "human",
                        "content": """Context: {info}"""
                    },
                    {
                    "type": "human",
                    "content": "Only output a single JSON BLOB with the dates as keys(which should always be in YYYY-MM-DD format) and the values as the objective for that date. keep the objective under 10 words. Do not select more than 4 days. Keep the first date as today if user has provided the today date.Also add the description short and crisp"
                    }
                ]

PROMPT_IMAGE = [
                    {
                        "type": "system",
                        "content": "Write me a short prompt for image generation. You will be provided with the context and theme for which the image will be generated for. Keep it short and to the point. Only provide one key 'prompt' with the prompt in output JSON"
                    },
                    {
                        "type": "human",
                        "content": "Context: {info}"
                    },
                    {
                    "type": "human",
                    "content": f"Please provide me the message inside a JSON BLOB"
                    }
                ]
IMAGE_NEG_PROMPT_OLD = "Human, Man, Woman, Child, hand, arms, fingers, kanji, italic,, Watermark, Text, censored, deformed, bad anatomy, disfigured, poorly drawn face, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers"
IMAGE_NEG_PROMPT_V2 = "Human, Man, Woman, Child, hand, Face"
IMAGE_NEG_PROMPT_V3 = "texts, sentences worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, mutilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur:1.3), (3D ,3D Game, 3D Game Scene, 3D Character:1.1), (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3)"
IMAGE_NEG_PROMPT = "Typography, Font, Calligraphy, watermark"