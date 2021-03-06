import ply.yacc as yacc
from DartLex import *
import DartSintaxeAbstrata as sa
import DartVisitor as vis
import DartSemanticVisitor as sv

def p_topLevelDefinition(p):
    ''' topLevel : variableDeclaration PCOMMA
                 | variableDeclaration PCOMMA topLevel
                 | functionSignature functionBody
                 | functionSignature functionBody topLevel
                 '''
    if len(p) == 3 and isinstance(p[1], sa.functionSignature):
        p[0] = sa.TopLevelDefinitionFunction(p[1], p[2])
    elif len(p) == 4 and isinstance(p[1], sa.functionSignature):
        p[0] = sa.TopLevelDefinitionFunctionRepetition(p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = sa.TopLevelDefinitionVariable(p[1])
    else:
        p[0] = sa.TopLevelDefinitionVariableRepetition(p[1], p[3])


def p_variableDeclaration(p):
    ''' variableDeclaration : declaredIdentifier
                            | variableDeclaration COMMA ID '''
    if len(p) == 2:
        p[0] = sa.VariableDeclarationID(p[1])
    else:
        p[0] = sa.ConcretevariableDeclaration(p[1],p[3])


def p_declaredIdentifier(p):
    ''' declaredIdentifier : type ID '''
    p[0] = sa.DeclaredIdentifierType(p[1],p[2])
              

def p_type(p):
    ''' type : VAR
             | INT
             | FLOAT
             | CHAR 
             | STRING
             | VOID
             | BOOLEAN'''
    p[0] = p[1]

def p_functionSignature(p):
    ''' functionSignature : ID formalParameterList
                          | type ID formalParameterList '''
    if(len(p) == 3):
        p[0] = sa.CallFormalParameterListId(p[1], p[2])
    else: 
        p[0] = sa.CallFormalParameterListvoidOrType(p[1], p[2], p[3])


def p_formalParameterList(p):
    ''' formalParameterList : LPAREN RPAREN 
                            | LPAREN normalFormalParameters RPAREN '''
    if len(p) == 4:
        p[0] = sa.CallNormalFormalParameters(p[2])
    else:
        p[0] = None


def p_normalFormalParameters(p):
    ''' normalFormalParameters : simpleFormalParameter 
                               | simpleFormalParameter COMMA normalFormalParameters '''
    if(len(p) == 2):
        p[0] = sa.CallNormalFormalParameter(p[1])
    else:
        p[0] = sa.NormalFormalParametersRepetition(p[1],p[3])


def p_simlpleFormalParameter(p):
    ''' simpleFormalParameter : type ID
                              | expression'''
    if(len(p) == 3):
        p[0] = sa.CallVoidOrType(p[1],p[2])
    else:
        p[0] = sa.CallParameterExpression(p[1])


def p_functionBody(p):
    ''' functionBody : block'''
    p[0] = sa.CallFunctionBody(p[1])


def p_block(p):
    ''' block : LCHAV statements RCHAV              
              | LCHAV RCHAV'''
    if len(p) == 4:
        p[0] = sa.CallBlockStatements(p[2])
    else:
        p[0] = sa.CallBlockStatements(None)

def p_statements(p):
    ''' statements : statement statements
                   | statement '''
    if(len(p) == 3):
        p[0] = sa.ConcretStatements(p[1], p[2])
    else:
        p[0] = sa.ConcretStatement(p[1])

def p_statement(p):
    ''' statement : nonLabelledStatement '''
    p[0] = sa.StatementNonLabelledStatement(p[1])


def p_nonLabelledStatement(p):
    ''' nonLabelledStatement : block
                             | expressionStatement
                             | localVariableDeclaration
                             | returnStatement
                             | ifStatement
                             | forStatement
                             | whileStatement
                             | doStatement
                             | switchStatement 
                             | breakStatement '''
    if isinstance(p[1], sa.expressionStatement):
        p[0] = sa.ConcreteExpressionStatement(p[1])
    elif(isinstance(p[1], sa.block)):
        p[0] = sa.NonLabelledStatementblock(p[1])
    elif(isinstance(p[1], sa.localVariableDeclaration)):
        p[0] = sa.LocalVariableDeclaration(p[1])
    elif(isinstance(p[1], sa.returnStatement)):
        p[0] = sa.ConcreteReturnStatement(p[1])
    elif(isinstance(p[1], sa.ifStatement)):
        p[0] = sa.ConcreteIfStatement(p[1]) 
    elif(isinstance(p[1], sa.forStatement)):
        p[0] = sa.ConcreteForStatement(p[1])
    elif(isinstance(p[1], sa.whileStatement)):
        p[0] = sa.ConcreteWhileStatement(p[1])
    elif(isinstance(p[1], sa.doStatement)):
        p[0] = sa.ConcreteDoStatement(p[1])
    elif(isinstance(p[1], sa.switchStatement)):
        p[0] = sa.ConcreteSwitchStatement(p[1])
    else:
        p[0] = sa.ConcreteBreakStatement(p[1])
    
    
def p_localVariableDeclaration(p):
    ''' localVariableDeclaration : initializedVariableDeclaration PCOMMA'''
    p[0] = sa.CallLocalInitializedVariableDeclaration(p[1])


def p_initializedVariableDeclaration(p):
    ''' initializedVariableDeclaration : declaredIdentifier
                                       | declaredIdentifier ATRIBUIR expression
                                       | literal ATRIBUIR expression
                                       | initializedVariableDeclaration COMMA ID '''
    if (len(p) == 2):
        p[0] = sa.CallDeclaredIdentifier(p[1])
    elif (len(p) == 4 and isinstance(p[3], sa.expression)):
        p[0] = sa.CallDeclaredInitializedIdentifier(p[1], p[3])
    elif (isinstance(p[1], sa.initializedVariableDeclaration) and p[2] == ','):
        p[0] = sa.CalliniRepeticion(p[1], p[3])
    else:
        p[0] = sa.CallLiteralAtribuirExp(p[1], p[3])


def p_expressionStatement(p):
    ''' expressionStatement : PCOMMA
                            | expression PCOMMA '''
    if len(p) == 3:
        p[0] = sa.Concretexpression(p[1])
    else:
        p[0] = p[1]


def p_expression(p): 
    ''' expression : orExpression'''
    p[0] = sa.CallExpression(p[1])

def p_orExpression(p):
    ''' orExpression : andExpression
                     | orExpression OR andExpression'''
    if (len(p) == 2):
        p[0] = sa.CallandExpression(p[1])
    else:
        p[0] = sa.ExpressionORexpression(p[1], p[2], p[3])


def p_andExpression(p):
    '''andExpression : equalityExpression
                     | andExpression AND equalityExpression'''
    if(len(p) == 2):
        p[0] = sa.CalligualExpression(p[1])
    else:
        p[0] = sa.CallAndExpressionIgual(p[1], p[2], p[3])

def p_equalityExpression(p):
    '''equalityExpression : relacionalExpression
                          | equalityExpression IGUAL relacionalExpression 
                          | equalityExpression NEG relacionalExpression '''
    
    if(len(p) == 2):
        p[0] = sa.CallRelacionalExpression(p[1])
    else:
        p[0] = sa.CallEqualityExpression(p[1], p[2], p[3])


def p_relacionalExpression(p):
    '''relacionalExpression : addExpression
                    | relacionalExpression MENOR addExpression
                    | relacionalExpression MAIOR addExpression
                    | relacionalExpression MENORI addExpression
                    | relacionalExpression MAIORI addExpression'''
    if(len(p) == 2):
        p[0] = sa.CallUnary(p[1])
    else:
        p[0] = sa.CallConcretExpression(p[1], p[2], p[3])


def p_addExpression(p):
    '''addExpression : multExpression 
                     | addExpression SOMA multExpression
                     | addExpression SUBTRAIR multExpression'''
    if(len(p) == 2):
        p[0] = sa.CallMultExpression(p[1])
    else:
        p[0] = sa.CallAddExpressionMult(p[1], p[2], p[3])


def p_multExpression(p):
    '''multExpression : unaryExpression 
                      | multExpression VEZES unaryExpression
                      | multExpression DIVIDIR unaryExpression
                      | multExpression RESTO unaryExpression'''
    if len(p) == 2:
        p[0] = sa.CallUnaryExp(p[1])
    else:
        p[0] = sa.CallUnaryExpMultExpression(p[1], p[2], p[3])
        

def p_unaryExpression(p):
    '''unaryExpression : primary
                       | functionCall
                       | unaryExpression SOMASOMA
                       | unaryExpression SUBSUB'''
                    
    if(len(p) == 2 and isinstance(p[1], sa.primary)):
        p[0] = sa.ConcreteprimaryExpression(p[1])
    elif (len(p) == 2 and isinstance(p[1], sa.functionCall)):
        p[0] = sa.Callfunctioncall(p[1])
    else:
        p[0] = sa.ConcreteunaryExpression(p[1], p[2])


def p_functionCall(p):
    '''functionCall : functionSignature'''
    p[0] = sa.ConcretFunctionCall(p[1])

def p_primary(p): 
    ''' primary : literal 
                | LPAREN expression RPAREN '''
    if len(p) == 2:
        p[0] = sa.CallPrimaryLiteral(p[1])
    else:
        p[0] = sa.CallPrimaryExpression(p[2])

def p_literal(p):
    ''' literal : ID 
                | booleanLiteral 
                | listLiteralID
                | listLiteral
                | NUMBER
                | FLOAT
                | LITERAL_STRING'''
    if (isinstance(p[1], str) and p[1].replace(".","").isdigit()):
        p[0] = sa.CallNum(p[1])
    elif isinstance(p[1],str) and (p[1][0] not in ["'", '"']):
        p[0] = sa.CallLiteralId(p[1])
    elif isinstance(p[1], str):
        p[0] = sa.CallLiteralString(p[1])
    elif len(p) == 2 and isinstance(p[1], sa.listLiteralID):
        p[0] = sa.CallLiteralListLiteralID(p[1])
    elif len(p) == 2 and isinstance(p[1], sa.booleanLiteral):
        p[0] = sa.CallLiteralBooleanLiteral(p[1])
    elif len(p) == 2 and isinstance(p[1], sa.listLiteral):
        p[0] = sa.CallLiteralListLiteral(p[1])


def p_listLiteral(p): 
    '''listLiteral : LCON expressionList RCON '''
    p[0] = sa.ExpressionListlistLiteral(p[2])

def p_listLiteralID(p): 
    '''listLiteralID : ID listLiteral'''
    p[0] = sa.CallListlistLiteralID(p[1], p[2])

def p_booleanLiteral(p): 
    ''' booleanLiteral : TRUE 
                       | FALSE '''
    if(len(p) == 2 and p[1] == 'TRUE'):
        p[0] = sa.booleanLiteralTrue(p[1])
    else:
        p[0] = sa.booleanLiteralFalse(p[1])


def p_expresionList(p):
    ''' expressionList : expression COMMA
                       | expression
                       | expression COMMA expressionList '''
    if len(p) == 2 or len(p) == 3:
        p[0] = sa.ConcreteExpression(p[1])
    else:
        p[0] = sa.CallExpressionList(p[1], p[3])


def p_returnStatement(p):
    ''' returnStatement : RETURN PCOMMA 
                        | RETURN expression PCOMMA'''
    p[0] = sa.ReturnStatementExpression(p[2])


def p_ifStatement(p):
    '''ifStatement : IF LPAREN expression RPAREN statement 
                   | IF LPAREN expression RPAREN statement ELSE statement '''
    if (len(p) == 6):
        p[0] = sa.IfexpressionStatement(p[1], p[3], p[5])
    else:
        p[0] = sa.IfElseExpressionStatement(p[1], p[3], p[5], p[6], p[7])


def p_forStatement(p):
    ''' forStatement : FOR LPAREN forLoopParts RPAREN statement '''
    p[0] = sa.ConcreteForLoopParts(p[1], p[3], p[5])


def p_forLoopParts(p):
    ''' forLoopParts : forInitializerStatement PCOMMA 
                     | forInitializerStatement PCOMMA expressionList 
                     | forInitializerStatement expression PCOMMA 
                     | forInitializerStatement expression PCOMMA expressionList '''
    if(len(p) == 3 and isinstance(p[1], sa.forInitializerStatement)):
        p[0] = sa.ConcreteForInitializerStatement(p[1])
    elif(p[2] == ';' and len(p) == 4):
        p[0] = sa.ForInitializerStatementExpressionList(p[1],p[3])
    elif(len(p) == 4 and p[3] == ';'):
        p[0] = sa.ForInitializerStatementExpression(p[1],p[2])
    else:
        p[0] = sa.ExpressionForInitializerStatementExpressionList(p[1],p[2],p[4])


def p_forInitializerStatement(p):
    ''' forInitializerStatement : localVariableDeclaration 
                                | PCOMMA 
                                | expression PCOMMA '''
    if (len(p) == 2 and p[1] != ';'):
        p[0] = sa.ConcreteForInitializerStatement(p[1])
    elif (len(p) == 3):
        p[0] = sa.CallConcreteExpression(p[1])
    else:
        p[0] = sa.CallConcreteExpression(None)


def p_whileStatement(p):
    ''' whileStatement : WHILE LPAREN expression RPAREN statement'''
    p[0] = sa.WhileStatementExpressionStatement(p[1],p[3],p[5])


def p_doStatement(p):
    ''' doStatement : DO statement WHILE LPAREN expression RPAREN PCOMMA '''
    p[0] = sa.DOStatementWhileExpression(p[1], p[2],p[3],p[5])


def p_switchStatement(p):
    ''' switchStatement : SWITCH LPAREN expression RPAREN LCHAV switchCaseRepetition RCHAV
                        | SWITCH LPAREN expression RPAREN LCHAV switchCaseRepetition defaultCase RCHAV'''
    if (len(p) == 8):
        p[0] = sa.ConcreteSwitch(p[1],p[3],p[6])
    else:
        p[0] = sa.ConcreteDefaultCase(p[1],p[3],p[6],p[7])


def p_switchCaseRepetition(p):
    ''' switchCaseRepetition : switchCase switchCaseRepetition
                             | switchCase '''
    if (len(p) == 3):
        p[0] = sa.RepetitionSwitchCase(p[1],p[2])
    else:
        p[0] = sa.RepetitionSwitchCase2(p[1])


def p_switchCase(p):
    ''' switchCase : CASE expression PONTOS statements '''
    p[0] = sa.ExpressionSwitchCase(p[1],p[2],p[4])


def p_defaultCase(p):
    ''' defaultCase : DEFAULT PONTOS statements '''
    if (len(p) == 4):
        p[0] = sa.DefaultStatements(p[1],p[3])
    else:
        p[0] = sa.LabelDefaultCase(p[1],p[2])


def p_breakStatement(p):
    ''' breakStatement : BREAK PCOMMA 
                       | BREAK ID PCOMMA'''
    if len(p) == 2:
        p[0] = sa.CallBreak(p[1])
    else:
        p[0] = sa.BreakID(p[1], p[2])


def p_error(p):
    print("Syntax error in input!")


lexer = lex.lex()
###############
#     Test it out     #
        ###############
data =  '''  

int soma(int parcela1, int parcela2, int parcela3){
    return parcela1 + parcela2 + parcela3 + 10;
 }
 
int subtracao(int valor1, int valor2){
    return valor1 - valor2;
}

float multiplicacao (float valor1, float valor2){
    return valor1 * valor2;
}

void main() {

    /*   DECLARAÇAO
        DE VARIAVEIS   */
        
    int par2, par3;
    int par1 = 50;
    par3 = 6;
    par2 = 50;

    float vl1 = 5.5;
    float vl2;
    vl2 = 6.5;

    int q = 8;
    int w = 10;

    int resposta;
    int outraResposta;

    //Observacao, tenha doh:
    String melhorProfessor = "Cabojinha";
    String precisoDeNota = "AJUDE A GENTE PROFESSOR";
 
    int escolha;
    
    if(q > w){
       do{
            switch(escolha){
                case 1:
                    for( int i = 0; i > 10 ; i ++)
                        soma(par1,par2,par3);
                    break;
                case 2:
                    while(w>q)
                        subtracao(par1,par2);
                    break;
                case 3:
                    for(int i = 0; i >10 ; i ++){
                        multiplicacao(vl1,vl2);
                        print(melhorProfessor);
                    }
                    break;
                default:
                    break;
                    print("Opção Incorreta! Escolha entre 1 e 3, por favor");
                    
            }
        }while(resposta == 9 && outraResposta != 7);
    }
    else
        print("Não foi possivel fazer suas contas"); 
} 
 
/* ****************************************
                OUTRO TESTE                
   **************************************** */

/*

int sumparabolac(int a){
    return a;
}

int sumparabola(int a, int b, int c){
    return a + b + true;
}

int some (int a, int b){
    a = 88 + 44;
    b = 70;
    sumparabola(1, 2, 3);        
    while (true){
        c = 38;
        sumparabola(5, true, false);
        while (c){
            sumparabola(5, true, true);
        }
    }
    sumparabolac(2);
    return true;
}

*/
'''

lexer.input(data)
parser = yacc.yacc()
result = parser.parse(debug=True)

visitor = sv.SemanticVisitor()
# visitor = vis.Visitor()
result.accept(visitor)

