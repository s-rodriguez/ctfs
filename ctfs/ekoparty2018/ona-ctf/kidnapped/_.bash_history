whoami
cd Desktop/
ls
cat /etc/passwd
sudo su -
cd /home/
su - eldiegomaradona
su - elcharliedelapeople
crontab -e
cd /home/alumno/
cd facu/
cd programacion_assembler/
cd tarea_final/
vim play_for_key.c
movcc play_for_key -o play_for_key
vim simd.asm
zip -er tarea_secuestrada.asm.zip simd.asm
rm -rf simd.asm play_for_key.c
openssl enc -aes-256-cbc -in tarea_secuestrada.asm.zip -out tarea_secuestrada.asm.zip.enc
openssl enc -aes-256-cbc -in play_for_key -out play_for_key.enc
rm -rf play_for_key
rm -rf tarea_secuestrada.asm.zip
vim nota
cd ~
rm .bash*
logout