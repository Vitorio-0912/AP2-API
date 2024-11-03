from config import db
from .turma_model import Turma
from datetime import datetime

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    dt_nasc = db.Column(db.Date)
    nt_primeiro_semestre = db.Column(db.Float)
    nt_segundo_semestre = db.Column(db.Float)
    media_final = db.Column(db.Float)
    
    turma = db.relationship('Turma', back_populates='alunos')

    def __init__(self, nome, idade, turma_id,  dt_nasc, nt_primeiro_semestre, nt_segundo_semestre):
        self.nome = nome
        self.idade = idade
        self.turma_id = turma_id
        self.dt_nasc = dt_nasc
        self.nt_primeiro_semestre = nt_primeiro_semestre
        self.nt_segundo_semestre = nt_segundo_semestre
        self.media_final = self.calcular_media_final()  # Calcular média ao criar o aluno

    def calcular_media_final(self):
       
        if self.nt_primeiro_semestre is not None and self.nt_segundo_semestre is not None:
            return (self.nt_primeiro_semestre + self.nt_segundo_semestre) / 2
        return None  

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'turma_id': self.turma_id,
            'dt_nasc': self.dt_nasc,
            'nt_primeiro_semestre': self.nt_primeiro_semestre,
            'nt_segundo_semestre': self.nt_segundo_semestre,
            'media_final': self.media_final
        }

class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dict()

def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

def adicionar_aluno(aluno_data):
    dt_nasc = aluno_data.get('dt_nasc')
    if isinstance(dt_nasc, str):
        dt_nasc = datetime.strptime(dt_nasc, '%Y-%m-%d').date()
    novo_aluno = Aluno(
        nome=aluno_data['nome'],
        idade=aluno_data.get('idade', None),  
        turma_id=aluno_data['turma_id'],
        dt_nasc=dt_nasc,  
        nt_primeiro_semestre=aluno_data.get('nt_primeiro_semestre', 0),  
        nt_segundo_semestre=aluno_data.get('nt_segundo_semestre', 0)  
    )
    db.session.add(novo_aluno)
    db.session.commit()

def atualizar_aluno(id_aluno, novos_dados):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    dt_nasc = novos_dados.get('dt_nasc')
    if isinstance(dt_nasc, str):
        dt_nasc = datetime.strptime(dt_nasc, '%Y-%m-%d').date()

    aluno.nome = novos_dados.get('nome', aluno.nome)  
    aluno.turma_id = novos_dados.get('turma_id', aluno.turma_id) 
    aluno.idade = novos_dados.get('idade', aluno.idade)  
    aluno.dt_nasc = dt_nasc  
    aluno.nt_primeiro_semestre = novos_dados.get('nt_primeiro_semestre', aluno.nt_primeiro_semestre)  
    aluno.nt_segundo_semestre = novos_dados.get('nt_segundo_semestre', aluno.nt_segundo_semestre)  
    aluno.media_final = aluno.calcular_media_final()  
    db.session.commit()

def excluir_aluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    db.session.delete(aluno)
    db.session.commit()