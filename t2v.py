from gradio_client import Client, handle_file

class T2VModel:
    def __init__(self, model_name: str = "THUDM/CogVideoX-5B-Space"):
        self.client = Client(model_name)

    def generate_video(self, prompt: str, video_strength: float = 0.8, seed_value: int = -1, scale_status: bool = False, rife_status: bool = False):
        """
        Generates a video based on the provided prompt.

        :param prompt: The text prompt describing the video.
        :param video_strength: The strength of the video generation effect.
        :param seed_value: Seed for reproducibility (-1 for random seed).
        :param scale_status: Whether to scale the video to fit the desired size.
        :param rife_status: Whether to use RIFE (video interpolation) for smoother videos.
        :return: Generated video result.
        """
        result = self.client.predict(
            prompt=prompt,
            image_input=None,
            video_input=None,
            video_strength=video_strength,
            seed_value=seed_value,
            scale_status=scale_status,
            rife_status=rife_status,
            api_name="/generate"
        )
        return result
