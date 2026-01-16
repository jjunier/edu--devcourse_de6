from typing import Any, Optional, List

class Node:
    def __init__(self, item: Any):
        """
        연결 리스트를 구성하는 노드를 초기화한다.

        Args:
            item (Any): 노드에 저장할 데이터
        """
        self.data = item
        self.next: Optional["Node"] = None

class LinkedList:
    def __init__(self):
        """
        단일 연결 리스트를 초기화한다.

        - 빈 리스트일 때:
            nodeCount == 0
            head == None
            tail == None
        - nodeCount > 0 일 때:
            head는 첫 번째 노드를,
            tail은 마지막 노드를 가리킨다.
        """
        self.nodeCount = 0
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    def traverse(self) -> List[Any]:
        """
        연결 리스트에 저장된 모든 데이터를 순서대로 리스트(배열)로 반환한다.

        Returns:
            list: 연결 리스트에 저장된 데이터들의 리스트
        """
        result: List[Any] = []
        curr = self.head
        
        while curr is not None:
            result.append(curr.data)
            curr = curr.next
        
        return result
    
    def getAt(self, pos: int) -> Optional[Node]:
        """
        지정한 위치(pos)에 있는 노드를 반환한다.

        노드의 위치를 1부터 시작한다
        - pos == 1         : head(첫 노드) 
        - pos == nodeCount : tail(마지막 노드)

        Args:
            pos (int): 삽입 기준이 되는 이전 노드 (1 이상 nodeCount 이하)
        
        Returns:
            Node or None: 해당 위치의 노드, 범위를 벗어나면 None
        """
        if pos < 1 or pos > self.nodeCount:
            return None
        
        i = 1
        curr = self.head

        while i < pos and curr is not None:
            curr = curr.next
            i += 1
        
        return curr
    
    def insertAt(self, pos: int, newNode: Node) -> bool:
        """
        지정한 위치(pos)에 newNode를 삽입한다.

        삽입 위치 pos는 1부터 시작한다.
        - pos == 1              : 맨 앞(head)에 삽입 (빈 리스트 포함)
        - pos == nodeCount + 1  : 맨 뒤(tail 뒤)에 삽입 (빈 리스트 포함)
        - 그 외                 : 중간 삽입 (반드시 prev 탐색 필요)

        Args:
            pos (int): 삽입 기준이 되는 이전 노드 (1 이상 nodeCount + 1 이하)
            newNode (Node): 새로 삽입할 노드
        
        Returns:
            bool: 삽입 성공 여부 (범위 밖이면 False)
        """
        if pos < 1 or pos > self.nodeCount + 1:
            return False

        # 1) 빈 리스트에 첫 삽입: head/tail 모두 newNode
        if self.nodeCount == 0:
            # pos는 반드시 1을 만족함
            self.head = newNode
            self.tail = newNode
            newNode.next = None
            self.nodeCount = 1

            return True

        # 2) 맨 앞에 삽입
        if pos == 1:
            newNode.next = self.head
            self.head = newNode
            self.nodeCount += 1

            return True

        # 3) 맨 뒤 삽입: O(1)으로 처리 가능
        if pos == self.nodeCount + 1:
            assert self.tail is not None # nodeCount > 0 이므로 tail은 존재해야 함
            self.tail.next = newNode
            newNode.next = None
            self.tail = newNode
            self.nodeCount += 1

            return True
        
        # 4) 중간 삽입: prev를 찾아 연결을 조작
        prev = self.getAt(pos - 1)
        if prev is None:
            return False
        
        newNode.next = prev.next
        prev.next = newNode
        self.nodeCount += 1

        return True
    
    def popAt(self, pos: int) -> Any:
        """
        지정한 위치(pos)의 노드를 제거하고 해당 데이터를 반환한다.

        삭제 위치는 1부터 시작한다.
        - pos == 1          : head 삭제
        - pos == nodeCount  : tail 삭제 (이전 노드 탐색 필요)
        - 그 외             : 중간 삭제 (이전 노드 탐색 필요)

        Args:
            pos (int): 제거할 노드의 위치 (1부터 시작)
            
        Returns:
            Any: 제거된 노드의 데이터
        
        Raises:
            IndexError: pos가 유효 범위를 벗어나면 발생
        """
        if pos < 1 or pos > self.nodeCount:
            raise IndexError("pos out of range")
        
        # nodeCount >= 1 이므로 head는 존재해야 함
        assert self.head is not None

        # 1) head 삭제
        if pos == 1:
            curr = self.head
            self.head = curr.next

            # 삭제 전 노드가 1개인 경우, 빈 리스트로 반환됨
            if self.nodeCount == 1:
                self.tail = None

            self.nodeCount -= 1
            curr.next = None
            
            return curr.data
        
        # 2) head가 아닌 위치 삭제: prev를 찾아 curr(삭제 대상)을 결정
        prev = self.getAt(pos - 1)
        
        if prev is None or prev.next is None:
            raise IndexError("pos out of range")
        
        curr = prev.next
        prev.next = curr.next

        # 3) tail 삭제 시, tail 갱신
        if pos == self.nodeCount:
            self.tail = prev
        
        self.nodeCount -= 1
        curr.next = None

        return curr.data
    
    def concat(self, L: "LinkedList") -> None:
        """
        현재 연결 리스트 뒤에 또 다른 연결 리스트 L을 연결한다.

        - 현재 리스트가 비어 있어도 정상 동작해야 한다.
        - L이 비어 있어도 정상 동작해야 한다.
        - 연결 후에는 L의 노드들이 현재 리스트의 뒤에 이어진다.

        Args:
            L (LinkedList): 현재 리스트 뒤에 이어 붙일 연결 리스트
        Returns:
            None
        """
        # L이 비어 있다면, 아무 변화 없음
        if L.nodeCount == 0:
            return
        
        # 현재 리스트가 비어 있다면, head/tail을 L로 그대로 가져옴
        if self.nodeCount == 0:
            self.head = L.head
            self.tail = L.tail
            self.nodeCount = L.nodeCount

            return
        
        # 둘 다 비어있지 않다면, tail 뒤에 이어 붙임
        assert self.tail is not None
        self.tail.next = L.head
        self.tail = L.tail
        self.nodeCount += L.nodeCount