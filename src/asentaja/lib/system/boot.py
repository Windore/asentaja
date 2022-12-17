import asentaja

class Boot:
    disable = False

    kernel_parameters = []

    # It is probably better if these hooks are not modified by any other option for now atleast.
    mkinitcpio_hooks = [ "base", "udev", "autodetect", "modconf", "kms", "keyboard", "keymap", "consolefont", "block", "filesystems", "fsck" ]
    mkinitcpio_modules = []
    mkinitcpio_files = []
    mkinitcpio_binaries = []
    mkinitcpio_extra_config = ""
    
    grub_default = 0
    grub_timeout = 5
    grub_extra_config = ""

    os_prober = False
    intel_microcode = False
    amd_microcode = False

    def apply(self):
        if not self.disable:
            grub_options = f"""# This file is auto-generated by asentaja
GRUB_DEFAULT={self.grub_default}
GRUB_TIMEOUT={self.grub_timeout}
GRUB_CMDLINE_LINUX_DEFAULT="{" ".join(self.kernel_parameters)}"
"""

            asentaja.packages += [ "grub", "efibootmgr" ]

            if self.os_prober:
                asentaja.packages += [ "os-prober" ]
                grub_options += "GRUB_DISABLE_OS_PROBER=false\n"
            else:
                grub_options += "GRUB_DISABLE_OS_PROBER=true\n"

            if self.intel_microcode:
                asentaja.packages += [ "intel-ucode" ]

            if self.amd_microcode:
                asentaja.packages += [ "amd-ucode" ]

            grub_options += self.grub_extra_config
            asentaja.file_mappings["/etc/default/grub"] = asentaja.FileMapping(content=grub_options)

            mkinitcpio_options = f"""# This file is auto-generated by asentaja
MODULES=({" ".join(self.mkinitcpio_modules)})
BINARIES=({" ".join(self.mkinitcpio_binaries)})
FILES=({" ".join(self.mkinitcpio_files)})
HOOKS=({" ".join(self.mkinitcpio_hooks)})
{self.mkinitcpio_extra_config}"""

            asentaja.file_mappings["/etc/mkinitcpio.conf"] = asentaja.FileMapping(content=mkinitcpio_options)
