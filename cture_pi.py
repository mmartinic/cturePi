import os
import re
import random
import pygame

class CturePi(object):

    def __init__(self, folder):
        self.picture_folder = folder
        self.file_list = self.get_all_picture_files()

        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

    def get_all_picture_files(self):
        file_list = []
        picture_name_pattern = re.compile('.+\.jpg$', re.I)

        for dirpath, dirnames, filenames in os.walk(self.picture_folder):
            file_list.extend([os.path.join(dirpath, f) for f in filenames if picture_name_pattern.match(f)])
        return file_list

    def knuth_shuffle(self):
        n = len(self.file_list)
        for i in range(n):
            k = random.randint(i, n - 1)
            temp = self.file_list[i]
            self.file_list[i] = self.file_list[k]
            self.file_list[k] = temp

    def resize_image(self, image, screen_height, screen_width):
        height = image.get_height()
        width = image.get_width()
        r = min(float(screen_height) / height, float(screen_width) / width)
        image = pygame.transform.scale(image, (int(width * r), int(height * r)))
        return image

    def show_image(self, image_file):
        image = pygame.image.load(image_file)

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        image = self.resize_image(image, screen_height, screen_width)

        self.screen.fill((0, 0, 0))
        self.screen.blit(image, ((screen_width - image.get_width()) / 2, (screen_height - image.get_height()) / 2))
        self.clock.tick(0.25)
        pygame.display.flip()

    def check_keypress_events(self):
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_w:
                    self.screen = pygame.display.set_mode((0, 0))
                elif event.key == pygame.K_f:
                    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        return done

    def main(self):
        done = False
        while not done:
            self.knuth_shuffle()
            for imageFile in self.file_list:
                done = self.check_keypress_events()

                if done:
                    break
                self.show_image(imageFile)

        pygame.quit()

if __name__ == '__main__':
    cture_pi = CturePi("/home/mmartinic/Pictures")
    cture_pi.main()