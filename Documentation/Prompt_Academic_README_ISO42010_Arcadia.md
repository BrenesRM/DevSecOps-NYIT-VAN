# Prompt académico para actualización de README

## Objetivo
Actualizar y mejorar el README del repositorio DevSecOps-NYIT-VAN con rigor académico, usando ISO/IEC 42010 y metodología Arcadia, incluyendo diagramas Mermaid (arquitectura y máquina de estados), referencias a ISO/IEC 330xx, ISO/IEC 42001, OWASP AI y OWASP Cybersecurity.

## Prompt sugerido (copiar y pegar)

Actúa como un comité académico de arquitectura de software y ciberseguridad.

Contexto del repositorio:
- Proyecto: DevSecOps-NYIT-VAN
- Dominio: seguridad de cadena de suministro de software con DevSecOps y detección asistida por IA
- Evidencia documental disponible en:
  - Documentation/Automating_Software_Supply_Chain_Security_AI_Powered_Threat_Detection_in_DevSecOps.pdf
  - Documentation/Marlon_Brenes_Rojas_SecDev2026_Academic_Brief_7202.pdf
  - project.tex
  - Documentation/PosterACM.png

Tarea:
1. Reescribe el README con estilo académico-profesional en español e inglés técnico cuando sea necesario.
2. Estructura el documento con enfoque ISO/IEC 42010:
   - Stakeholders
   - Concerns
   - Viewpoints
   - Views
   - Architectural decisions y rationale
   - Trazabilidad de decisiones y riesgos
3. Organiza el contenido con enfoque Arcadia (Need, Operational, System, Logical, Physical).
4. Incluye diagramas Mermaid obligatorios:
   - Un diagrama de arquitectura (flowchart o C4 simplificado)
   - Un flujo CI/CD de seguridad
   - Una máquina de estados del ciclo operativo (stateDiagram-v2)
5. Agrega sección de evaluación y mejora de procesos con ISO/IEC 330xx:
   - Capacidad de proceso actual (cualitativa si no hay métricas numéricas)
   - Recomendaciones de mejora por nivel
6. Agrega sección de gobernanza de IA con ISO/IEC 42001:
   - Riesgos de IA en detección automatizada
   - Controles de gestión y supervisión humana
7. Agrega sección OWASP:
   - OWASP para ciberseguridad de aplicaciones y pipeline (SAST/DAST/SCA/Secrets)
   - OWASP AI para riesgos específicos de sistemas con IA
8. Construye una sección "Resultados y evidencia" usando exclusivamente hallazgos verificables en el repositorio y la carpeta Documentation.
9. Inserta el póster ACM en el README usando Markdown:
   - ![Poster ACM Conference](Documentation/PosterACM.png)
10. No inventes métricas. Si faltan datos, crea una subsección "Métricas pendientes" con lista de datos recomendados para futuras iteraciones.

Criterios de calidad:
- Claridad académica
- Coherencia entre arquitectura, riesgos y controles
- Evidencia trazable a archivos reales
- Mermaid válido y renderizable en GitHub
- Redacción final apta para revisión universitaria y comité técnico

Formato de salida requerido:
- Entregar el README completo listo para reemplazar el existente.
- Mantener una tabla de contenido navegable.
- Incluir una sección final "Limitaciones y trabajo futuro".
