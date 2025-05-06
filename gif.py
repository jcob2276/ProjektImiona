from moviepy.editor import VideoFileClip

def convert_mp4_to_gif(input_file, output_file):
    video = VideoFileClip(input_file)
    video.write_gif(output_file, fps=10)
    video.close()

input_file1 = r"C:\Users\jakub\Desktop\bar_race_imiona_zenskie.mp4"
input_file2 = r"C:\Users\jakub\Desktop\bar_race_imiona_meskie.mp4"
output_file1 = r"C:\Users\jakub\Desktop\bar_race_imiona_zenskie.gif"
output_file2 = r"C:\Users\jakub\Desktop\bar_race_imiona_meskie.gif"

convert_mp4_to_gif(input_file1, output_file1)
convert_mp4_to_gif(input_file2, output_file2)

print("Konwersja zakończona!")