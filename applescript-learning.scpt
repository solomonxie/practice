FasdUAS 1.101.10   ��   ��    k             l     ��������  ��  ��        l     ��������  ��  ��     	 
 	 l      ��  ��    Z T
-- Hello world
tell current application
    display dialog "Hello World."
end tell
     �   � 
 - -   H e l l o   w o r l d 
 t e l l   c u r r e n t   a p p l i c a t i o n 
         d i s p l a y   d i a l o g   " H e l l o   W o r l d . " 
 e n d   t e l l 
 
     l     ��������  ��  ��        l     ��������  ��  ��        l     ��������  ��  ��        l      ��  ��    k e
-- Variables
set str to "MacOS"
tell current application
    display dialog "Hello " & str
end tell
     �   � 
 - -   V a r i a b l e s 
 s e t   s t r   t o   " M a c O S " 
 t e l l   c u r r e n t   a p p l i c a t i o n 
         d i s p l a y   d i a l o g   " H e l l o   "   &   s t r 
 e n d   t e l l 
      l     ��������  ��  ��        l     ��������  ��  ��        l     ��������  ��  ��         l      �� ! "��   ! K E
--Empy trash
tell application "Finder"
    empty the trash
end tell
    " � # # � 
 - - E m p y   t r a s h 
 t e l l   a p p l i c a t i o n   " F i n d e r " 
         e m p t y   t h e   t r a s h 
 e n d   t e l l 
    $ % $ l     ��������  ��  ��   %  & ' & l     ��������  ��  ��   '  ( ) ( l      �� * +��   * � �
-- Display notification
display notification "All graphics have been converted." with title "My Graphic Processing Script" subtitle "Processing is complete." sound name "Frog"
    + � , ,b 
 - -   D i s p l a y   n o t i f i c a t i o n 
 d i s p l a y   n o t i f i c a t i o n   " A l l   g r a p h i c s   h a v e   b e e n   c o n v e r t e d . "   w i t h   t i t l e   " M y   G r a p h i c   P r o c e s s i n g   S c r i p t "   s u b t i t l e   " P r o c e s s i n g   i s   c o m p l e t e . "   s o u n d   n a m e   " F r o g " 
 )  - . - l     ��������  ��  ��   .  / 0 / l     ��������  ��  ��   0  1 2 1 l      �� 3 4��   3 � �
-- Speak text
say "Sheet sheel bore"

say "Just what do you think you're doing Dave?" using "Alex" speaking rate 140 pitch 42 modulation 60
    4 � 5 5 
 - -   S p e a k   t e x t 
 s a y   " S h e e t   s h e e l   b o r e " 
 
 s a y   " J u s t   w h a t   d o   y o u   t h i n k   y o u ' r e   d o i n g   D a v e ? "   u s i n g   " A l e x "   s p e a k i n g   r a t e   1 4 0   p i t c h   4 2   m o d u l a t i o n   6 0 
 2  6 7 6 l     ��������  ��  ��   7  8 9 8 l     ��������  ��  ��   9  : ; : l     ��������  ��  ��   ;  < = < l     �� > ?��   > !  Prompt to choose file name    ? � @ @ 6   P r o m p t   t o   c h o o s e   f i l e   n a m e =  A B A l     �� C D��   C H B set fname to choose file name with prompt "Save the document as:"    D � E E �   s e t   f n a m e   t o   c h o o s e   f i l e   n a m e   w i t h   p r o m p t   " S a v e   t h e   d o c u m e n t   a s : " B  F G F l     ��������  ��  ��   G  H I H l     ��������  ��  ��   I  J K J l     �� L M��   L #  Display content of clipboard    M � N N :   D i s p l a y   c o n t e n t   o f   c l i p b o a r d K  O P O l     �� Q R��   Q %  display dialog (the clipboard)    R � S S >   d i s p l a y   d i a l o g   ( t h e   c l i p b o a r d ) P  T U T l     ��������  ��  ��   U  V W V l     ��������  ��  ��   W  X Y X l     �� Z [��   Z   Run shell commands    [ � \ \ &   R u n   s h e l l   c o m m a n d s Y  ] ^ ] l     �� _ `��   _   do shell script "ls -la"    ` � a a 2   d o   s h e l l   s c r i p t   " l s   - l a " ^  b c b l     ��������  ��  ��   c  d e d l     �� f g��   f $  Display notification (simple)    g � h h <   D i s p l a y   n o t i f i c a t i o n   ( s i m p l e ) e  i�� i l     j���� j I    �� k��
�� .sysonotfnull��� ��� TEXT k m      l l � m m B A l l   g r a p h i c s   h a v e   b e e n   c o n v e r t e d .��  ��  ��  ��       �� n o��   n ��
�� .aevtoappnull  �   � **** o �� p���� q r��
�� .aevtoappnull  �   � **** p k      s s  i����  ��  ��   q   r  l��
�� .sysonotfnull��� ��� TEXT�� �j ascr  ��ޭ
