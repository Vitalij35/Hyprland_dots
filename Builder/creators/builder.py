import os
import packages

from logger import Logger, LoggerStatus
from creators.software import AurBuilder
from creators.software import FirefoxCustomize
from creators.patches import PatchSystemBugs
from creators.daemons import Daemons

# TODO: Implement error handling for package installation

class SystemConfiguration:
    def start(*args):
        start_text = f"[+] Starting assembly. Options {args}"
        Logger.add_record(start_text, status=LoggerStatus.SUCCESS)
        if args[0]: SystemConfiguration.__start_option_1()
        if args[1]: SystemConfiguration.__start_option_2()
        if args[2]: SystemConfiguration.__start_option_3()
        if args[3]: SystemConfiguration.__start_option_4()
        # TODO: The process should not be repeated when reassembling, important components should only be updated with new ones
        Daemons.enable_all_daemons()
        PatchSystemBugs.enable_all_patches()

    @staticmethod
    def __start_option_1():
        SystemConfiguration.__create_default_folders()
        SystemConfiguration.__copy_bspwm_dotfiles()

    @staticmethod
    def __start_option_2():
        Logger.add_record("[+] Updates Enabled", status=LoggerStatus.SUCCESS)
        os.system("sudo pacman -Sy")

    @staticmethod
    def __start_option_3():
        Logger.add_record("[+] Installed hyprland Dependencies", status=LoggerStatus.SUCCESS)
        AurBuilder.build()
        SystemConfiguration.__install_pacman_package(packages.BASE_PACKAGES)
        SystemConfiguration.__install_aur_package(packages.AUR_PACKAGES)
        FirefoxCustomize.build()

    @staticmethod
    def __start_option_4():
        Logger.add_record("[+] Installed Dev Dependencies", status=LoggerStatus.SUCCESS)
        SystemConfiguration.__install_pacman_package(packages.DEV_PACKAGES)

    @staticmethod
    # TODO: Make a universal function for installing packages
    # TODO: Catch errors if the software is not detected
    def __install_pacman_package(package_names: list):
        for package in package_names:
            os.system(f"sudo pacman -S --noconfirm {package}")
            Logger.add_record(f"Installed: {package}", status=LoggerStatus.SUCCESS)

    @staticmethod
    # TODO: Make a universal function for installing packages
    # TODO: Catch errors if the software is not detected
    def __install_aur_package(package_names: list):
        for package in package_names:
            os.system(f"yay -S --noconfirm {package}")
            Logger.add_record(f"Installed: {package}", status=LoggerStatus.SUCCESS)

    @staticmethod
    def __create_default_folders():
        Logger.add_record("[+] Create default directories", status=LoggerStatus.SUCCESS)
        default_folders = "~/Media ~/Documents ~/Downloads " + \
                          "~/Music ~/Desktop ~/Other ~/Pictures " + \
                          "~/Projects ~/temp"
        os.system("mkdir -p ~/.config")
        os.system(f"mkdir -p {default_folders}")
        os.system("cp -r wallpapers/ ~/Pictures/")

    @staticmethod
    def __copy_bspwm_dotfiles():
        Logger.add_record("[+] Copy Dotfiles", status=LoggerStatus.SUCCESS)
        os.system("cp -r config/* ~/.config/")
        os.system("cp -r bin/ ~/")
