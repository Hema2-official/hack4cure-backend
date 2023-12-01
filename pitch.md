Sziasztok! 
Egy négy gimnazistából álló csapat vagyunk, és az EESZT egy fundamentális problémájára szeretnénk megoldást kínálni.

Abból a problémából indultunk ki, hogy az orvosoknak sok idejét veszi el a leletek és zárójelentések megírása. Tudjuk, hogy az egészségügyünkben a betegekről eleve sok információt tudunk, és ezek az adatok pedig az EESZT-ben van eltárolva. Ezt ki lehetne használni arra, hogy a dokumentumok létrehozásakor a orvos számára biztosított felületen a rendszer több mezőt eleve kitöltsön, valamint akár automatikus kitöltési lehetőségeket biztosítson a programozók által használt GitHub Copilothoz hasonlóan, gyorsítva a munkáját.

Viszont itt egy olyan problémába ütköztünk, hogy az EESZT-ben az adatok nem strukturálva, hanem elsősorban PDF formátumban vannak, tehát azokat nehéz erre a célra feldolgozni, szűrni. Az alapötletünk az lenne, hogy a PDF-eket átalakítjuk strukturált formába, és egy olyan rendszert biztosítunk, ahol az új dokumentumokat az orvosok már az új strukturált formba tudják felvinni.

Az EESZT újraalapozása strukturált adatokra viszont az eredeti problémánkon, a dokumentumok kitöltésén kívül, lehetőséget tárházát nyitja meg az egészségügy hatékonyabbá tételére, amelyekből szeretnénk párat bemutatni.

Lehetővé tenné az adatok logikai validációját, ami nagyon egyszerű automatikus ellenőrzéseket hajthatna végre például arra, hogy nőnek ne lehessen prosztatarákja a rendszerben.

A halálos betegségek diagnosztikájában is előrelépést tudnánk elérni. Dani trainelt egy AI modellt a számunkra a szervezők által biztosított egészen limitált OMOP adatbázis alapján, ami 5 rizikófaktor alapján képes eldönteni, hogy kit lenne érdemes szűrővizsgálatra beutalni, és ehhez pusztán strukturált adatokra van szükség.

Ezen ötletek bármelyikére egy demonstrációt pár nap alatt létre lehet hozni.

Ami pedig a teljes fejlesztést illeti: folyamatos átállás során hajtanánk végre, ahol a PDF-eket mindig csak igény szerint konvertálnánk át, így időben megoszolna a terhelés a rendszeren.

A rendszerre 24 óra alatt létrehoztunk egy, az EESZT-t imitáló demonstrációt is, ami képes a strukturált formok kezelésére, PDF-ek átalakítására és strukturált adatbevitelre is, ami bizonyítja, hogy a feljesztés rövid idő alatt, egyszerűen végrehajtható. A fenti link segítségével akár meg is lehet tekinteni.
