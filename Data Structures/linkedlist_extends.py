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

        더미(dummy) head 노드를 사용한다.
        - 실제 데이터는 head.next부터 시작한다.
        - 빈 리스트일 경우:
            nodeCount == 0 
            head.next == None
            tail == head (더미 head를 tail로 둬서 경계 조건을 단순화)
        """
        self.nodeCount = 0
        self.head = Node(None)  # 맨 앞에 dummy node를 추가
        self.tail = self.head   # 빈 리스트에서는 tail이 더미 head를 가리킴
        self.head.next = None

    def traverse(self) -> List[Any]:
        """
        연결 리스트에 저장된 모든 데이터를 순서대로 리스트(배열)로 반환한다.

        더미 head 노드는 데이터에 포함하지 않는다.

        Returns:
            list: 연결 리스트에 저장된 데이터들의 리스트
        """
        result: List[Any] = []
        curr = self.head.next   # 첫 실제 데이터 노드부터 시작
        
        while curr is not None:
            result.append(curr.data)
            curr = curr.next
        
        return result
    
    def getAt(self, pos: int) -> Optional[Node]:
        """
        지정한 위치(pos)에 있는 노드를 반환한다.

        더미 head를 0번 인덱스로 취급한다.
        - pos == 0 : 더미 head 노드를 반환
        - pos == 1 : 첫 번째 실제 데이터 노드를 반환
        - pos == nodeCount : 마지막 실제 데이터 노드를 반환

        Args:
            pos (int): 삽입 기준이 되는 이전 노드 (0 이상 nodeCount 이하)
        
        Returns:
            Node or None: 해당 위치의 노드, 범위를 벗어나면 None
        """
        if pos < 0 or pos > self.nodeCount:
            return None
        
        i = 0   # head (dummy node는 0번) | getAt(0) -> head
        curr: Optional[Node] = self.head

        while i < pos and curr is not None:
            curr = curr.next
            i += 1
        
        return curr
    
    def insertAfter(self, prev: Node, newNode: Node) -> bool:
        """
        주어진 노드 prev의 뒤에 newNode를 삽입한다.

        이 함수는 '연결(포인터) 조작'의 핵심 로직을 담당한다.
        위치 탐색(몇 번째에 넣기)은 insertAt에서 수행하고,
        실제 삽입(링크 변경 + tail/nodeCount 갱신)은 해당 함수에서 수행된다.

        Args:
            prev (Node): 삽입 기준이 되는 이전 노드
            newNode (Node): 새로 삽입할 노드
        
        Returns:
            bool: 삽입 성공 여부
        """
        newNode.next = prev.next
        prev.next = newNode
        # prev가 tail이었다면, 새 노드가 마지막 노드가 됨
        if prev is self.tail:
            self.tail = newNode
        
        self.nodeCount += 1

        return True

    def insertAt(self, pos: int, newNode: Node) -> bool:
        """
        주어진 위치(pos)에 newNode를 삽입한다.

        pos는 실제 데이터 노드 기준으로 1부터 시작한다.
        - pos == 1              : 맨 앞(더미 head 바로 뒤)에 삽입
        - pos == nodeCount + 1  : 맨 뒤(현재 tail 뒤)에 삽입

        구현은 다음 2단계로 나뉜다.
        1) pos에 해당하는 '이전 노드(prev)'를 찾는다.
        2) insertAfter(prev, newNode)로 실제 삽입(링크 조작)을 수행한다.

        Args:
            pos (int): 삽입 기준이 되는 이전 노드 (1 이상 nodeCount + 1 이하)
            newNode (Node): 새로 삽입할 노드
        
        Returns:
            bool: 삽입 성공 여부
        """
        if pos < 1 or pos > self.nodeCount + 1:
            return False
        # 맨 뒤 삽입은 tail을 prev로 사용하면 O(1)
        if pos == self.nodeCount + 1:
            prev = self.tail

        else:
            # pos-1 위치의 노드가 prev (pos==1이면 prev는 더미 head)
            prev = self.getAt(pos - 1)
        
        if prev is None:
            return False
        
        return self.insertAfter(prev, newNode)
    
    def popAfter(self, prev: Node) -> Optional[Any]:
        """
        주어진 노드 prev의 '다음 노드'를 제거하고, 제거된 데이터 값을 반환한다.

        이 함수는 삭제 연산의 핵심 로직(링크 조작 + tail/nodeCount 갱신)을 담당한다.
        위치 탐색(몇 번째를 지울지)은 popAt에서 수행하고,
        실제 삭제는 해당 함수에서 수행한다.

        Args:
            prev (Node): 삭제 대상 노드의 이전 노드

        Returns:
            Any or None: 제거된 노드의 데이터 혹은 삭제할 노드가 없다면 None
        """
        curr = prev.next
        # 삭제할 노드가 없는 경우
        if curr is None:
            return None
        
        prev.next = curr.next
        # 지운 노드가 마지막 노드였다면 tail을 prev로 이동
        if curr is self.tail:
            self.tail = prev
        
        self.nodeCount -= 1
        curr.next = None

        return curr.data

    def popAt(self, pos: int) -> Any:
        """
        지정한 위치(pos)의 노드를 제거하고 해당 데이터를 반환한다.

        pos는 실제 데이터 노드 기준으로 1부터 시작한다.

        Args:
            pos (int): 제거할 노드의 위치 (1부터 시작)
            
        Returns:
            Any: 제거된 노드의 데이터
        
        Raises:
            IndexError: pos가 유효 범위를 벗어나면 발생
        """
        if pos < 1 or pos > self.nodeCount:
            raise IndexError("pos out of range")
        
        prev = self.getAt(pos - 1)

        if prev is None:
            raise IndexError("pos out of range")
        
        data = self.popAfter(prev)

        if data is None:
            raise IndexError("pos out of range")

        return data
    
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
        # L이 빈 리스트일 경우
        if L.nodeCount == 0:
            return
        
        # 현재 리스트가 비어 있다면, head.next를 L의 첫 노드로 연결
        if self.nodeCount == 0:
            self.head.next = L.head.next
            self.tail = L.tail
            self.nodeCount = L.nodeCount
            
            return 
        
        # 둘 다 빈 리스트가 아닐 경우, tail 뒤에 연결
        self.tail.next = L.head.next
        self.tail = L.tail
        self.nodeCount += L.nodeCount