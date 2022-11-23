if __name__ == '__main__':
    print("1.Black and White \n2.Colored")
    choice = int(input())
    file_name = input("File name (or 0 to get from webcam) : ")
    font_size = int(input("Font size : "))
    height_video = int(input("Video height : "))
    if choice == 1:
        if file_name == '0':
            from BlackWhitefromCam import ASCIIArtGeneratorCam

            process = ASCIIArtGeneratorCam(font_size=font_size, rows=height_video)
        else:
            from BlackWhite import ASCIIArtGenerator

            process = ASCIIArtGenerator(file_name, font_size=font_size, rows=height_video)
    else:
        n_bit_color = int(input("Color pallete : "))
        if file_name == '0':
            from ColoredfromCam import ASCIIArtGeneratorColoredCam

            process = ASCIIArtGeneratorColoredCam(font_size=font_size, rows=height_video, n_bits_color=n_bit_color)
        else:
            from Colored import ASCIIArtGeneratorColored

            process = ASCIIArtGeneratorColored(file_name, font_size=font_size, rows=height_video,
                                               n_bits_color=n_bit_color)
    process.run()
